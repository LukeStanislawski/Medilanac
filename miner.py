import sys, os
import crypt, config
import json, urllib3, time

class Miner():
	def __init__(self):
		self.blockchain = []
		self.priv, self.pub = crypt.gen_keys()
		self.chain_id = crypt.hash(self.pub)
		self.chain_dir = os.path.join(config.blockchain_dir, self.chain_id[:8])
		os.makedirs(self.chain_dir)

		self.http = urllib3.PoolManager()
		self.main()


	def main(self):
		self.blockchain.append(self.gen_genesis())
		
		for i in range(config.num_blocks):
			block = self.gen_new_block()
			chunks = self.fragment(json.dumps(block, sort_keys=True))

			# self.publish_block(self.blockchain[-1])
			self.publish_chunks(chunks, len(self.blockchain))
			block["foreign_chunks"] = self.get_foreign_chunks()

			self.blockchain.append(block)

			with open(self.chain_dir + "/blockchain.json", 'w') as f:
				f.write(json.dumps(self.blockchain, sort_keys=True, indent=4))




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


	def fragment(self, block):
		data = json.dumps(block, sort_keys=True)
		chunks = []
		start_i = 0

		while start_i < len(data):
			end_i = min(start_i + config.max_chunk_size, len(data))
			chunks.append(data[start_i:end_i])
			start_i = end_i

		return chunks


	def publish_chunk(self, chunk):
		accepted = False
		timeout = config.chunk_sub_timout

		while not accepted and timeout > 0:
			try:
				r = self.http.request('POST', config.chunk_sub_addr,
	                 headers={'Content-Type': 'application/json'},
	                 body=json.dumps(chunk))

				response = json.loads(r.data)
				if response["status"] == "accepted":
					accepted = True
			
			except Exception as e:
				print (str(e))
				accepted = False
			
			timeout -= 1
			time.sleep(config.miner_wait)

		if not accepted:
			print("Error: exchange submission timeout for miner {}".format(self.chain_id[:8]))


	def publish_chunks(self, chunk_data, block_id):
		for chunk_i, data in enumerate(chunk_data):
			chunk = {}
			chunk["head"] = {}
			chunk["head"]["chain_id"] = self.chain_id
			chunk["head"]["block_id"] = block_id
			chunk["head"]["chunk_id"] = chunk_i
			chunk["data"] = data
			chunk["hash"] = self.hash_chunk(chunk)
			chunk["signature"] = crypt.sign(self.priv, chunk['hash'])
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
				chunks.append(response)
			
			except Exception as e:
				print ("Error when retrieveing foreign chunks:")
				print (str(e))
			
			timeout -= 1
			time.sleep(config.miner_wait)

		return chunks