import sys, os
import crypt, config
from data_generator import gen_sample_data
import json, urllib3, time
from zfec import easyfec
from miner_server import Server
from multiprocessing import Process


class Miner():
	def __init__(self, id, server_port):
		self.id = id
		self.server_port = server_port
		self.blockchain = []
		self.priv, self.pub = crypt.gen_keys()
		self.chain_id = crypt.hash(self.pub)
		self.chain_dir = os.path.join(config.blockchain_dir, self.chain_id[:8])
		os.makedirs(self.chain_dir)

		self.http = urllib3.PoolManager()
		self.encoder = easyfec.Encoder(config.ec_k, config.ec_m)
		self.decoder = easyfec.Encoder(config.ec_k, config.ec_m)

		p = Process(target=Server, args=[self.id, server_port])
		p.start()

		self.main()
		time.sleep(1000)
		p.join()


	def main(self):
		self.blockchain.append(self.gen_genesis())
		print("Miner {}: In itialised and genesis block added to chain. PubKey hash: {}..".format(self.id, self.chain_id[:8]))

		
		for block_id in range(len(self.blockchain), config.num_blocks):
			block = self.gen_new_block()
			chunks = self.get_chunks(block, block_id)
			self.publish_chunks(chunks)
			print("Miner {}: Published chunks for block {}".format(self.id, block_id))
			block["foreign_chunks"] = self.get_foreign_chunks()
			print("Miner {}: Downloaded all foreign chunks for block {}".format(self.id, block_id))
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
		block["body"] = gen_sample_data(1)
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


	def publish_chunk(self, chunk):
		accepted = False
		timeout = config.chunk_sub_timout
		chunk_str = json.dumps(chunk, sort_keys=True)

		while not accepted and timeout > 0:
			try:
				r = self.http.request('POST', config.chunk_sub_addr,
	                 headers={'Content-Type': 'application/json'},
	                 body=chunk_str)

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


	def publish_chunks(self, chunks):
		for chunk_i, chunk in enumerate(chunks):
			self.publish_chunk(chunk)


	def get_foreign_chunks(self):
		chunks = []
		timeout = config.foreign_chunk_timout
		data_out = {}
		data_out["blacklist"] = [self.chain_id]

		while len(chunks) < config.num_foreign_chunks and timeout > 0:
			try:
				r = self.http.request('POST', config.chunk_ret_addr,
	                 headers={'Content-Type': 'application/json'},
	                 body=json.dumps(data_out))
				
				response = json.loads(r.data)
				if response != []:
					chunks.append(response)
			
			except Exception as e:
				print ("Error when retrieveing foreign chunks:")
				print (str(e))
			
			timeout -= 1
			time.sleep(config.miner_wait)

		if len(chunks) < config.num_foreign_chunks:
			print("Warning: could not find enough chunks ({}/{}) ({})".format(len(chunks), config.num_foreign_chunks, self.chain_id[:8]))

		return chunks


	def write_blockchain(self):
		with open(self.chain_dir + "/blockchain.json", 'w') as f:
			f.write(json.dumps(self.blockchain, sort_keys=True, indent=4))
