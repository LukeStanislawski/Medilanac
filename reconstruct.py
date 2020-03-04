import sys, os
import json
from zfec.easyfec import Decoder
from utils import crypt
from utils.config import Config



def main(branch_id):
	branch_paths = get_bpaths()
	chunks = find_chunks(branch_id, branch_paths)
	blocks = reconstruct_blocks(chunks)
	print (json.dumps(blocks, indent=4))
	write_chain(blocks)


def reconstruct(branch_id):
	branch_paths = get_bpaths()
	chunks = find_chunks(branch_id, branch_paths)
	blocks = reconstruct_blocks(chunks)
	return blocks
	

def get_bpaths():
	d = Config.blockchain_dir
	branch_dirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
	branch_paths = [os.path.join(d, "blockchain.json") for d in branch_dirs]
	return branch_paths


def find_chunks(branch_id, branch_paths):
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


def reconstruct_blocks(chunks):
	b_ids_found = sorted(list(set([x["head"]["block_id"] for x in chunks])))
	print ("Found chunks for blocks: {}".format(b_ids_found))

	blocks = []
	for b_id in b_ids_found:
		try:
			b_chunks = [x for x in chunks if x["head"]["block_id"] == b_id]
			print("Found {} chunks for block {}".format(len(b_chunks), b_id))
			b_chunks = sorted(b_chunks, key = lambda x: x['head']["chunk_id"])
			raw_chunks = [bytes(x["data"], 'utf-8') for x in b_chunks]
			inds = [x["head"]["chunk_id"] for x in b_chunks]

			d = Decoder(Config.ec_k, Config.ec_m)
			d_data = d.decode(raw_chunks[:Config.ec_k], inds[:Config.ec_k], 0)
			d_data = d_data.decode('utf-8').rstrip('\x00')
			blocks.append(json.loads(d_data))
		except Exception as e:
			print("Error, could not reconstruct block {}:".format(b_id))
			print(str(e))
			blocks.append({})

	return blocks


def write_chain(blocks):
	chain_id = blocks[-1]["head"]["chain_id"]
	chain_dir = os.path.join(Config.blockchain_dir, chain_id[:8])
	os.makedirs(chain_dir)
	with open(chain_dir + "/blockchain.json", 'w') as f:
		f.write(json.dumps(blocks, sort_keys=True, indent=4))



if __name__ == "__main__":
	chain_id = sys.argv[1]
	main(chain_id)