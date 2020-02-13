import sys, os
import random, time, json
import urllib3
from zfec import easyfec
from multiprocessing import Process
from utils import crypt, config
from utils.data_generator import gen_sample_data
from utils.miner_server import Server


class Miner():
	def __init__(self, id, server_port):
		self.id = id
		self.server_port = server_port
		self.blockchain = []
		self.priv, self.pub = crypt.gen_keys()
		self.chain_id = crypt.hash(self.pub)
		self.chain_dir = os.path.join(config.blockchain_dir, self.chain_id[:8])
		os.makedirs(self.chain_dir)
		with open(self.chain_dir + "/chunks.json", 'w') as f: f.write("[]")

		self.http = urllib3.PoolManager()
		self.encoder = easyfec.Encoder(config.ec_k, config.ec_m)
		self.decoder = easyfec.Encoder(config.ec_k, config.ec_m)

		p = Process(target=Server, args=[self.id, self.chain_id, server_port])
		p.start()

		self.main()
		time.sleep(1000)
		p.join()


	def main(self):
		self.publish_existence()
		genesis = self.gen_genesis()
		self.blockchain.append(genesis)
		self.write_blockchain()
		print("Miner {}: Initialised and genesis block added to chain. PubKey hash: {}..".format(self.id, self.chain_id[:8]))
		chunks = self.get_chunks(genesis, 0)
		self.write_chunks(chunks)


		for block_id in range(len(self.blockchain), config.num_blocks):
			if block_id == 0:
				block = self.gen_genesis()
			else:
				block = self.gen_new_block()

			chunks = self.get_chunks(block, block_id)
			self.write_chunks(chunks)

			block["foreign_chunks"] = self.get_foreign_chunks()
			self.blockchain.append(block)
			self.write_blockchain()
			print("Miner {}: Added block {} to chain".format(self.id, block_id))


		self.write_blockchain()
		print("Miner {}: Terminated".format(self.id))



	def gen_genesis(self):
		block = {}
		block["head"] = {}
		block["head"]["chain_id"] = self.chain_id
		block["head"]["id"] = 0
		block["body"] = "This is the first block in the blockchain"
		return block


	def gen_new_block(self):
		block = {}
		block["head"] = {}
		block["head"]["prev_block_hash"] = self.hash_block(self.blockchain[-1], include_fc=True)
		block["head"]["chain_id"] = self.chain_id
		block["head"]["id"] = len(self.blockchain)
		# block["body"] = gen_sample_data(1)
		block["body"] = crypt.get_rand_str()
		return block


	def hash_block(self, block, include_fc=False):
		raw_block = {}
		attrs = ["head", "body"]
		if include_fc: attrs.append("foreign_chunks")

		for attr in attrs:
			if attr in raw_block:
				raw_block[attr] = block[attr]

		return crypt.hash(json.dumps(raw_block, sort_keys=True))


	def hash_chunk(self, chunk):
		raw_chunk = {}
		for attr in ["head", "data"]:
			raw_chunk[attr] = chunk[attr]

		return crypt.hash(json.dumps(raw_chunk, sort_keys=True))


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
			chunk["hash"] = self.hash_chunk(chunk)
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

			try:
				r = self.http.request('POST', address,
	                 headers={'Content-Type': 'application/json'},
	                 body="{}")
				
				response = json.loads(r.data)
				if "status" not in response:
					chunks.append(response)
			
			except Exception as e:
				print ("Error when retrieveing foreign chunk from miner {} at {}:".format(miner["id"][:8], miner["address"]))
				print (str(e))
			
			timeout -= 1
			time.sleep(config.miner_wait)

		if len(chunks) < config.num_foreign_chunks:
			print("Warning: could not find enough chunks ({}/{}) ({})".format(len(chunks), config.num_foreign_chunks, self.chain_id[:8]))

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
				print ("Error when publishing chunks:")
				print (str(e))
				accepted = False
			
			timeout -= 1
			time.sleep(config.miner_wait)

		if not accepted:
			print("Error: exchange submission timeout for miner {}".format(self.chain_id[:8]))



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
				print ("Error when retrieveing foreign chunks:")
				print (str(e))
			
			timeout -= 1
			time.sleep(config.miner_wait)

		if len(miners) < 1:
			print("Warning: could not miners list from exchange")

		return miners


	def pick_miner(self):
		miners = self.get_miners()
		miners = [x for x in miners if x["id"] != self.chain_id]
		c = random.randint(0, len(miners)-1)
		return miners[c]
