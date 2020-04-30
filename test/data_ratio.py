import sys, os
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from utils.config import Config
import json
import numpy as np


def main():
	"""
	Calculates the average data ratio of block size to primary data size for all blocks on the network,
	"""
	block_lens = []
	data_lens = []
	head_lens = []
	fc_lens = []
	fc_body_lens = []

	# Get list of all blockchain directories
	dirs = os.listdir(Config.blockchain_dir)
	dirs = [x for x in dirs if not x.startswith(".")]

	# Iterate over each directory
	for bc_dir in dirs:
		# Read blockchain in directory
		with open(os.path.join(Config.blockchain_dir, bc_dir, "blockchain.json")) as f:
			bc = json.loads(f.read())

		# Iterate over each block in blockchhain
		for bi, block in enumerate(bc):
			# Ignore genesis block
			if bi != 0:
				# Record results to respective lists
				block_lens.append(len(json.dumps(block)))
				data_lens.append(len(block["body"]))
				head_lens.append(len(json.dumps(block["head"])))
				fc_lens.append(len(json.dumps(block["foreign_chunks"])))
				fc_body_lens.append(sum([len(x["data"]) for x in block["foreign_chunks"]]))
				

	# Create results (dict) object
	outdict = {}	
	outdict["block_lens"] = calc_list(block_lens, "Block length")
	outdict["data_lens"] = calc_list(data_lens, "Data length")
	outdict["head_lens"] = calc_list(head_lens, "Head length")
	outdict["fc_lens"] = calc_list(fc_lens, "Foreign chunk length")
	outdict["fc_body_lens"] = calc_list(fc_body_lens, "Foreign chunk body length")
	outdict["mean"] = np.mean([float(a)/float(b) for (a,b) in zip(block_lens, data_lens)])

	print("Block/data length ratio: {}".format(outdict["mean"]))

	# Write to file
	with open(Config.dr_res_file, "a") as f:
		f.write("{}\n".format(json.dumps(outdict)))



def calc_list(l, label):
	"""
	Given a list of results, generates min, mean, and max. Results als printed to screen.

	l: list of results
	label: The list label to be printed to screen
	"""
	outdict = {}
	outdict["min"] = min(l)
	outdict["mean"] = np.mean(l)
	outdict["max"] = max(l)
	print("{}: {} - {} - {}".format(label, outdict["min"], outdict["mean"], outdict["max"]))
	return outdict


if __name__ == "__main__":
	main()
