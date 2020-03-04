import sys, os
import random
import time
import json
import urllib3
from zfec import easyfec
from multiprocessing import Process
from utils import crypt
from utils.config import Config
from utils.data_generator import gen_sample_data
from utils.merkle import merkle_tree
from utils.validator import validate_headders
from miner.miner_log import MinerLog as Log
from miner.miner_server import Server


class Miner():
	def __init__(self, id, server_port, terminate_server=False):
		self.id = id
		self.server_port = server_port
		self.blockchain = []
		self.priv, self.pub = crypt.gen_keys()
		self.chain_id = crypt.hash(self.pub)
		self.chain_dir = os.path.join(Config.blockchain_dir, self.chain_id[:8])
		os.makedirs(self.chain_dir)
		with open(self.chain_dir + "/chunks.json", 'w') as f: f.write("[]")

		Log.set_up(self.id, self.chain_dir)

		self.http = urllib3.PoolManager()
		self.encoder = easyfec.Encoder(Config.ec_k, Config.ec_m)
		self.decoder = easyfec.Decoder(Config.ec_k, Config.ec_m)

		self.p_server = Process(target=Server, args=[self.id, self.chain_id, server_port, self.chain_dir])


		self.main()
	
		if terminate_server:
			time.sleep(1000)
			p.terminate()


	def main(self):
		Log.info("Initialised. PubKey hash: {}..".format(self.id, self.chain_id[:8]))

		# Generate genesis block
		genesis = self.gen_genesis()
		self.blockchain.append(genesis)
		self.write_blockchain()

		# Make chunks available
		Log.debug("Making chunks available")
		chunks = self.get_chunks(genesis, 0)
		self.write_chunks(chunks)

		# Start the miner server
		Log.debug("Starting miner server")
		self.p_server.start()

		# Publish miner/branch existance to exchange for peer discovery
		self.publish_existence()

		# Generate a specific number of blocks as definied in Config
		for block_id in range(len(self.blockchain), Config.num_blocks):			
			Log.debug("Generation of block {} commenced".format(block_id))
			if block_id == 0:
				block = self.gen_genesis()
			else:
				block = self.gen_new_block()

			# Generate chunks and make available
			chunks = self.get_chunks(block, block_id)
			self.write_chunks(chunks)

			# Update block with chunk data
			block["foreign_chunks"] = self.get_foreign_chunks()
			block = self.update_chunk_merkle(block)

			# Store and save block
			self.blockchain.append(block)
			self.write_blockchain()

			Log.info("Added block {} to chain".format(block_id))
		
		self.write_blockchain()
		Log.info("Terminated with {} chunks left to publish".format(self.id, len(self.load_local_chunks())))


	def gen_genesis(self):
		Log.debug("Generating genesis block")
		block = {}
		block["head"] = {}
		block["head"]["chain_id"] = self.chain_id
		block["head"]["id"] = 0
		block["head"]["pub_key"] = self.pub.hex()
		block["body"] = "This is the genesis block, the first block on the blockchain"
		
		return block


	def gen_new_block(self):
		Log.debug("Generating new block {}".format(len(self.blockchain)))
		block = {}
		block["head"] = {}
		block["head"]["prev_block_hash"] = crypt.hash_block(self.blockchain[-1])
		block["head"]["prev_block_head_hash"] = crypt.hash_block(self.blockchain[-1], attrs=["head"])
		block["head"]["chain_id"] = self.chain_id
		block["head"]["pub_key"] = self.pub.hex()
		block["head"]["id"] = len(self.blockchain)
		block["body"] = gen_sample_data(num_items=Config.data_items_per_block, rand_str=True, size=6)
		block["head"]["file_merkle"] = merkle_tree(block["body"])
		block["head"]["chunk_merkle"] = [] # Updated later
		block["head"]["signature"] = ""
		
		return block


	def get_chunks(self, block, block_id):
		Log.debug("Generating chunks from block {}".format(block_id))
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
		Log.debug("Updating chunks in file")
		with open(self.chain_dir + "/chunks.json") as f:
			e_chunks = json.loads(f.read())
		
		e_chunks.extend(chunks)
		
		with open(self.chain_dir + "/chunks.json", 'w') as f:
			f.write(json.dumps(e_chunks, indent=4))


	def get_foreign_chunks(self):
		Log.debug("Attempting top retrieve foreign chunks")
		chunks = []
		timeout = Config.foreign_chunk_timout + Config.num_foreign_chunks

		while len(chunks) < Config.num_foreign_chunks and timeout > 0:
			miner = self.pick_miner()
			address = miner["address"] + "/get-chunk"
			Log.debug("Fetching chunk from {}".format(address))

			try:
				Log.debug("Posting to {}".format(address))
				r = self.http.request('POST', address,
	                 headers={'Content-Type': 'application/json'},
	                 body="{}")
				
				Log.debug("Received response")
				response = json.loads(r.data)
				Log.debug("Parsed response JSON")
				if "status" not in response:
					chunks.append(response)
					Log.debug("Chunk retrieved from {}".format(address))
			
			except Exception as e:
				Log.warning("Error when retrieving foreign chunk from miner {} at {}:".format(miner["id"][:8], miner["address"]))
				Log.warning(str(e))
			
			timeout -= 1
			time.sleep(Config.miner_wait)

		if len(chunks) < Config.num_foreign_chunks:
			Log.info("Chunks received: ({}/{}) ({})".format(len(chunks), Config.num_foreign_chunks, self.chain_id[:8]))

		return chunks


	def write_blockchain(self):
		Log.debug("Writing blockchain")
		with open(self.chain_dir + "/blockchain.json", 'w') as f:
			f.write(json.dumps(self.blockchain, sort_keys=True, indent=4))


	def publish_existence(self):
		Log.debug("Publishing existence to exchange")
		data_out = {}
		data_out["branch_id"] = self.chain_id
		data_out["branch_address"] = "http://{}:{}".format(Config.exchange_ip, self.server_port)
		accepted = False
		timeout = Config.miner_exist_timout

		while not accepted and timeout > 0:
			try:
				Log.debug("Posting to {}".format(Config.miner_sub_addr))
				r = self.http.request('POST', Config.miner_sub_addr,
	                 headers={'Content-Type': 'application/json'},
	                 body=json.dumps(data_out))

				Log.debug("Received response: {}".format(r.data))
				response = json.loads(r.data)
				Log.debug("Parsed response JSON")
				if response["status"] == "accepted":
					accepted = True
			
			except Exception as e:
				Log.warning("Error when publishing chunks:")
				Log.warning(str(e))
				accepted = False
			
			timeout -= 1
			time.sleep(Config.miner_wait)

		if not accepted:
			Log.warning("Exchange submission timeout for miner {}".format(self.chain_id[:8]))


	def get_miners(self):
		Log.debug("Attempting to retrieve miners list from exchange")
		miners = []
		timeout = Config.retrieve_miners_timout

		while len(miners) < 1 and timeout > 0:
			try:
				Log.debug("Posting to {}".format(Config.get_miners_addr))
				r = self.http.request('POST', Config.get_miners_addr,
	                 headers={'Content-Type': 'application/json'},
	                 body="{}")
				
				Log.debug("Received response: {}".format(r.data))
				miners = json.loads(r.data)
				Log.debug("Parsed response JSON")

			except Exception as e:
				Log.warning("Error when retrieving foreign chunks:")
				Log.warning(str(e))
			
			timeout -= 1
			time.sleep(Config.miner_wait)

		Log.debug("Retrieved {} miners from exchange".format(len(miners)))
		if (len(miners) < 1) or (len(miners) == 1 and miners[0]["id"] == self.chain_id):
			Log.warning("Could not get miners list from exchange")

		return miners


	def pick_miner(self):
		Log.debug("Picking miner")
		valid = False
		
		while not valid:
			miners = self.get_miners()
			miners = [x for x in miners if x["id"] != self.chain_id]
			miner = miners[random.randint(0, len(miners)-1)]
			valid = self.validate_miner(miner)
		
		Log.debug("Chosed miner {} at {}".format(miner["id"], miner["address"]))
		return miner


	def validate_miner(self, miner):
		Log.debug("Validating miner {}".format(miner["id"]))
		blockchain = self.fetch_headders(miner["address"])
		es = validate_headders(blockchain)
		
		if len(es) > 0:
			Log.debug("Blockchain INVALID:{}".format("\n    ".join(es)))
			return False
		else:
			Log.debug("Blockchain VALID")
			return True


	def fetch_headders(self, addr):
		Log.debug("Fetching headers from {}".format(addr))
		blockchain = None
		try:
			Log.debug("Posting to {}".format(addr + "/blockchain-headders"))
			r = self.http.request('POST', addr + "/blockchain-headders",
                 headers={'Content-Type': 'application/json'},
                 body="{}")
			
			Log.debug("Received response: {}".format(r.data))
			blockchain = json.loads(r.data)
			Log.debug("Parsed response JSON")

		except Exception as e:
			Log.warning("Error when retreiveing foreign chunks:")
			Log.warning(str(e))
		
		return blockchain


	def load_local_chunks(self):
		Log.debug("Loading local chunks from file")

		with open(os.path.join(self.chain_dir, "chunks.json")) as f:
			chunks = json.loads(f.read())
		
		return chunks


	def update_chunk_merkle(self, block):
		Log.debug("Updating chunk merkle tree from block {}".format(block["head"]["id"]))
		hashes = [x["hash"] for x in block["foreign_chunks"]]
		merkle = merkle_tree(hashes)
		block["head"]["chunk_merkle"] = merkle[0:-1]
		
		return block
