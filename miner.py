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
		block["head"]["prev_block_hash"] = self.hash_block(self.blockchain[-1])
		block["head"]["chain_id"] = self.chain_id
		block["head"]["id"] = len(self.blockchain)
		block["body"] = crypt.get_rand_str()
		return block


	def hash_block(self, block):
		raw_block = {}
		for attr in ["head", "body"]:
			raw_block[attr] = block[attr]

		return crypt.hash(json.dumps(raw_block, sort_keys=True))


	def hash_chunk(self, chunk):
		raw_chunk = {}
		for attr in ["head", "data"]:
			raw_chunk[attr] = chunk[attr]

		return crypt.hash(json.dumps(raw_chunk, sort_keys=True))


	def fragment(self, block):
		data = json.dumps(block, sort_keys=True)
		max_chunk_size = 100
		chunks = []
		start_i = 0

		while start_i < len(data):
			end_i = min(start_i + max_chunk_size, len(data))
			chunks.append(data[start_i:end_i])
			start_i = end_i

		return chunks
		

	def publish_chunk(self, chunk):
		accepted = False
		timeout = config.block_sub_timout

		while not accepted and timeout > 0:
			try:
				r = self.http.request('POST', config.exchange_addr + '/submit',
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
			chunk["head"]["branch_id"] = self.chain_id
			chunk["head"]["block_id"] = block_id
			chunk["head"]["chunk_id"] = chunk_i
			chunk["data"] = data
			chunk["hash"] = self.hash_chunk(chunk)
			chunk["signature"] = crypt.sign(self.priv, chunk['hash'])

			self.publish_chunk(chunk)