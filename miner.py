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
		self.gen_genesis()

		for block_num in range(config.num_blocks):
			self.gen_new_block()
			self.publish_block(self.blockchain[-1])

			with open(self.chain_dir + "/blockchain.json", 'w') as f:
				f.write(json.dumps(self.blockchain, sort_keys=True, indent=4))


	def gen_genesis(self):
		genesis_block = {}
		genesis_block["body"] = "This is the first block in the blockchain"
		self.blockchain.append(genesis_block)


	def gen_new_block(self):
		block = {}
		block["head"] = {}
		block["head"]["prev_block_hash"] = self.hash_block(self.blockchain[-1])
		block["head"]["chain_id"] = self.chain_id
		block["head"]["id"] = len(self.blockchain)
		block["body"] = crypt.get_rand_str()
		self.blockchain.append(block)


	def hash_block(self, block):
		for attr in block:
			if attr not in ["head", "body"]:
				del block[attr]

		return crypt.hash(json.dumps(block, sort_keys=True))


	def publish_block(self, block):
		accepted = False
		timeout = config.block_sub_timout

		while not accepted and timeout > 0:
			try:
				r = self.http.request('POST', config.exchange_addr + '/submit',
	                 headers={'Content-Type': 'application/json'},
	                 body=json.dumps(block))
				
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
