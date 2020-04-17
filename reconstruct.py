import sys, os
import json
from zfec.easyfec import Decoder
from utils import crypt
from utils.config import Config



def main(branch_id, buf=0):
	"""
	Reconstruct the primary data of a branch from foreign chunks on other branches

	branch_id: ID of the branch to attempt to reconstruct
	"""
	branch_paths = get_bpaths()
	chunks = find_chunks(branch_id, branch_paths)
	blocks = reconstruct_blocks(chunks, buf)
	print("Reconstructed blockchain:")
	print (json.dumps(blocks, indent=4))
	write_chain(blocks)


def reconstruct(branch_id, buf=0):
	"""
	Reconstruct the primary data of a branch from foreign chunks on other branches
	Returns blockchain data struct instead of printing and savingto file

	branch_id: ID of the branch to attempt to reconstruct
	"""
	branch_paths = get_bpaths()
	chunks = find_chunks(branch_id, branch_paths)
	blocks = reconstruct_blocks(chunks, buf)
	return blocks
	

def get_bpaths():
	"""
	Returns a list of all file paths of blockchain JSON files
	"""
	d = Config.blockchain_dir
	branch_dirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
	branch_paths = [os.path.join(d, "blockchain.json") for d in branch_dirs]
	return branch_paths


def find_chunks(branch_id, branch_paths):
	"""
	Searches for all foreign chunks on blockchains relating to a specific branch

	branch_id: The ID of the branch to search for foreign chunks from
	branch_paths: List of json files to search
	"""
	chunks = []

	for path in branch_paths:
		with open(path) as f:
			blockchain = json.loads(f.read())

			for block in blockchain:
				if "foreign_chunks" in block:
					for chunk in block["foreign_chunks"]:
						if chunk["head"]["chain_id"].startswith(branch_id):
							chunks.append(chunk)

	return chunks


def reconstruct_blocks(chunks, buf=0):
	"""
	Sort chhunks and attempt to reconstruct the original data of each block that chunks were found for

	chunks: List of chunks to use for reconstruction
	"""
	# Create sorted list of all block IDs found
	b_ids_found = sorted(list(set([x["head"]["block_id"] for x in chunks])))
	print ("Found chunks for blocks: {}".format(b_ids_found))

	blocks = []
	# Ignore any chunks relating to the late <buf> number discovered
	if buf != 0:
		b_ids_found = b_ids_found[:(-1 * buf)]
	print("Testing: {}".format(b_ids_found))

	# Attempt to reconstruct each block
	for b_id in b_ids_found:
		print(" BLock id: {}".format(b_id))

		# Get chunks for this block only
		b_chunks = [x for x in chunks if x["head"]["block_id"] == b_id]
		print("Found {} chunks for block {}".format(len(b_chunks), b_id))
		
		# Ensure no duplicates
		b_chunks = list(set([json.dumps(x, sort_keys=True) for x in b_chunks]))
		b_chunks = [json.loads(x) for x in b_chunks]

		# Sort chunks
		b_chunks = sorted(b_chunks, key = lambda x: x['head']["chunk_id"])
		raw_chunks = [bytes(x["data"], 'cp437') for x in b_chunks]
		inds = [x["head"]["chunk_id"] for x in b_chunks]

		# Reconstruct using inverse erasure coding
		d = Decoder(Config.ec_k, Config.ec_m)
		print(inds[:Config.ec_k])
		d_data = d.decode(raw_chunks[:Config.ec_k], inds[:Config.ec_k], 0)
		d_data = d_data.decode('utf-8').rstrip('\x00')
		blocks.append(json.loads(d_data))

	return blocks


def write_chain(blocks):
	"""
	Writes reconstructed blockchain to file
	"""
	if len(blocks) > 0:
		chain_id = blocks[-1]["head"]["chain_id"]
		chain_dir = os.path.join(Config.blockchain_dir, chain_id[:8])
		os.makedirs(chain_dir)
		with open(chain_dir + "/blockchain.json", 'w') as f:
			f.write(json.dumps(blocks, sort_keys=True, indent=4))
	else:
		print("Error: Could not write blockchain to file as blockchain is empty")



if __name__ == "__main__":
	chain_id = sys.argv[1]

	if len(sys.argv) > 2:
		buf = int(sys.argv[2])
	else:
		buf = 0

	main(chain_id, buf=buf)