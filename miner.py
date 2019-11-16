import sys, os
import crypt
import json

class Miner():
	def __init__(self):
		self.priv, self.pub = crypt.gen_keys()
		self.chain_id = crypt.hash(self.pub)
		self.blockchain = []
		self.chain_dir = os.path.join(os.path.dirname(__file__), "data", "blockchain", self.chain_id[:8])
		os.makedirs(self.chain_dir)
		self.run()


	def run(self):
		genesis_block = {}
		genesis_block["body"] = "This is the first block in the blockchain"
		self.blockchain.append(genesis_block)

		for block_num in range(5):
			block = {}
			block["head"] = {}
			block["head"]["prev_block_hash"] = self.hash_block(self.blockchain[-1])
			block["head"]["chain_id"] = self.chain_id
			block["body"] = crypt.get_rand_str()
			self.blockchain.append(block)

		with open(self.chain_dir + "/blockchain.json", 'w') as f:
			f.write(json.dumps(self.blockchain, sort_keys=True, indent=4))


	def hash_block(self, block):
		for attr in block:
			if attr not in ["head", "body"]:
				del block[attr]

		return crypt.hash(json.dumps(block, sort_keys=True))
