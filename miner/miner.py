import sys, os
import random, time, json
import urllib3
from zfec import easyfec
from multiprocessing import Process
from utils import crypt
from utils.config import Config
from utils.data_generator import gen_sample_data
from utils.merkle import merkle_tree
from utils.logging import Log
from miner.miner_server import Server


log = Log()
config = Config()


class Miner():
	def __init__(self, id, server_port, test=False):
		self.id = id
		self.server_port = server_port
		self.blockchain = []
		self.priv, self.pub = crypt.gen_keys()
		self.chain_id = crypt.hash(self.pub)
		self.chain_dir = os.path.join(config.blockchain_dir, self.chain_id[:8])
		os.makedirs(self.chain_dir)
		with open(self.chain_dir + "/chunks.json", 'w') as f: f.write("[]")

		log.set_up(self.id, self.chain_dir)

		self.http = urllib3.PoolManager()
		self.encoder = easyfec.Encoder(config.ec_k, config.ec_m)
		self.decoder = easyfec.Decoder(config.ec_k, config.ec_m)

		self.p_server = Process(target=Server, args=[self.id, self.chain_id, server_port, self.chain_dir])

		if not test:
			self.main()
		
			time.sleep(1000)
			p.join()


	def main(self):
		log.info("Initialised. PubKey hash: {}..".format(self.id, self.chain_id[:8]))

		# Generate genesis block
		log.debug("Generating genesis block")
		genesis = self.gen_genesis()
		self.blockchain.append(genesis)
		self.write_blockchain()

		# Make chunks available
		log.debug("Making chunks available")
		chunks = self.get_chunks(genesis, 0)
		self.write_chunks(chunks)

		# Start the miner server
		log.debug("Starting miner server")
		self.p_server.start()
		# Publish miner/branch existance to exchange for peer discovery
		log.debug("Publishing existence")
		self.publish_existence()

		# Generate a specific number of blocks as definied in config
		for block_id in range(len(self.blockchain), config.num_blocks):			
			log.debug("Generation of block {} commenced".format(block_id))
			if block_id == 0:
				block = self.gen_genesis()
			else:
				block = self.gen_new_block()

			# Generate chunks and make available
			log.debug("Generating chunks and writing to file")
			chunks = self.get_chunks(block, block_id)
			self.write_chunks(chunks)

			# Update block with chunk data
			log.debug("Updating block with chunk data")
			block["foreign_chunks"] = self.get_foreign_chunks()
			block = self.update_chunk_merkle(block)

			# Store and save block
			log.debug("Storing and saving block")
			self.blockchain.append(block)
			self.write_blockchain()

			log.info("Added block {} to chain".format(block_id))
		
		self.write_blockchain()
		log.info("Terminated with {} chunks left to publish".format(self.id, len(self.load_local_chunks())))


	def gen_genesis(self):
		block = {}
		block["head"] = {}
		block["head"]["chain_id"] = self.chain_id
		block["head"]["id"] = 0
		block["body"] = "This is the genesis block, the first block on the blockchain"
		return block


	def gen_new_block(self):
		block = {}
		block["head"] = {}
		block["head"]["prev_block_hash"] = crypt.hash_block(self.blockchain[-1])
		block["head"]["prev_block_head_hash"] = crypt.hash_block(self.blockchain[-1], attrs=["head"])
		block["head"]["chain_id"] = self.chain_id
		block["head"]["id"] = len(self.blockchain)
		block["body"] = gen_sample_data(num_items=config.data_items_per_block, rand_str=True, size=6)
		block["head"]["file_merkle"] = merkle_tree(block["body"])
		block["head"]["chunk_merkle"] = [] # Updated later
		return block


	def get_chunks(self, block, block_id):
		chunks = []
		data = json.dumps(block, sort_keys=True).encode('utf-8')
		c_datas = self.encoder.encode(data)
		c_datas = [x.decode('cp437') for x in c_datas]

		for ci, c_data in enumerate(c_datas):
			chunk = {}
			chunk["head"] = {}
			chunk["head"]["chain_id"] = self.chain_id
			chunk["head"]["block_id"] = block_id
			chunk["head"]["chunk_id"] = ci
			chunk["data"] = c_data
			chunk["hash"] = crypt.hash_chunk(chunk)
			chunk["signature"] = crypt.sign(self.priv, chunk['hash'])
			chunks.append(chunk)

		return chunks


	def write_chunks(self, chunks):
		with open(self.chain_dir + "/chunks.json") as f:
			e_chunks = json.loads(f.read())
		e_chunks.extend(chunks)
		with open(self.chain_dir + "/chunks.json", 'w') as f:
			f.write(json.dumps(e_chunks, indent=4))


	def get_foreign_chunks(self):
		chunks = []
		timeout = config.foreign_chunk_timout + config.num_foreign_chunks

		while len(chunks) < config.num_foreign_chunks and timeout > 0:
			miner = self.pick_miner()
			address = miner["address"] + "/get-chunk"
			log.debug("Fetching chunk from {}".format(address))

			try:
				r = self.http.request('POST', address,
	                 headers={'Content-Type': 'application/json'},
	                 body="{}")
				
				response = json.loads(r.data)
				if "status" not in response:
					chunks.append(response)
					log.debug("Chunk retrieved from {}".format(address))
			
			except Exception as e:
				log.warning("Error when retrieveing foreign chunk from miner {} at {}:".format(miner["id"][:8], miner["address"]))
				log.warning(str(e))
			
			timeout -= 1
			time.sleep(config.miner_wait)

		if len(chunks) < config.num_foreign_chunks:
			log.info("Chunks recieved: ({}/{}) ({})".format(len(chunks), config.num_foreign_chunks, self.chain_id[:8]))

		return chunks


	def write_blockchain(self):
		with open(self.chain_dir + "/blockchain.json", 'w') as f:
			f.write(json.dumps(self.blockchain, sort_keys=True, indent=4))


	def publish_existence(self):
		data_out = {}
		data_out["branch_id"] = self.chain_id
		data_out["branch_address"] = "http://{}:{}".format(config.exchange_ip, self.server_port)
		accepted = False
		timeout = config.miner_exist_timout

		while not accepted and timeout > 0:
			try:
				r = self.http.request('POST', config.miner_sub_addr,
	                 headers={'Content-Type': 'application/json'},
	                 body=json.dumps(data_out))

				response = json.loads(r.data)
				if response["status"] == "accepted":
					accepted = True
			
			except Exception as e:
				log.warning("Error when publishing chunks:")
				log.warning(str(e))
				accepted = False
			
			timeout -= 1
			time.sleep(config.miner_wait)

		if not accepted:
			log.warning("Exchange submission timeout for miner {}".format(self.chain_id[:8]))



	def get_miners(self):
		miners = []
		timeout = config.retrieve_miners_timout

		while len(miners) < 1 and timeout > 0:
			try:
				r = self.http.request('POST', config.get_miners_addr,
	                 headers={'Content-Type': 'application/json'},
	                 body="{}")
				
				miners = json.loads(r.data)
			except Exception as e:
				log.warning("Error when retrieveing foreign chunks:")
				log.warning(str(e))
			
			timeout -= 1
			time.sleep(config.miner_wait)

		if len(miners) < 1:
			log.warning("Could not get miners list from exchange")

		return miners


	def pick_miner(self):
		valid = False
		while not valid:
			miners = self.get_miners()
			miners = [x for x in miners if x["id"] != self.chain_id]
			miner = miners[random.randint(0, len(miners)-1)]
			valid = self.validate_miner(miner)
			valid = True
		return miner


	def validate_miner(self, miner):
		blockchain = self.fetch_headders(miner["address"])
		return True


	def fetch_headders(self, addr):
		blockchain = None
		try:
			r = self.http.request('POST', addr + "/blockchain-headders",
                 headers={'Content-Type': 'application/json'},
                 body="{}")
			
			blockchain = json.loads(r.data)
		except Exception as e:
			log.warning("Error when retrieveing foreign chunks:")
			log.warning(str(e))
		
		return blockchain


	def load_local_chunks(self):
		with open(os.path.join(self.chain_dir, "chunks.json")) as f:
			chunks = json.loads(f.read())
		return chunks


	def update_chunk_merkle(self, block):
		hashes = [x["hash"] for x in block["foreign_chunks"]]
		merkle = merkle_tree(hashes)
		block["head"]["chunk_merkle"] = merkle[0:-1]
		return block
