import sys, os
import json
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import crypt
from utils.merkle import merkle


def validate_blockchain(blockchain):
	es = []

	es.extend(v_prev_head_hash(blockchain))
	es.extend(v_single_chainid(blockchain))
	es.extend(v_merkle_trees(blockchain))

	return es


def validate_headders(blockchain):
	es = []

	es.extend(v_prev_head_hash(blockchain))
	es.extend(v_single_chainid(blockchain))
	es.extend(v_merkle_trees(blockchain))

	return es


def v_structure(blockchain, attrs=["head", " body", "foreign_chunks"]):
	es = []

	# Check blockchain is list
	if type(blockchain) is not list:
		es.append("Incorrect blockchain format, expected list but recieved {}".format(
			type(blockchain)))
		return es


	for bi, block in enumerate(blockchain):
		# Check each block is dict
		if type(block) is not dict:
			es.append("Block {} is not type dict but is {}".format(bi, type(block)))
			continue

		# Check each block contains the required fields
		if bi == 0 and "head" not in block:
			es.append("Genesis block does not contain 'head' field")
		else:
			for attr in attrs:
				if attr not in block:
					es.append("Block {} does not contain '{}' field".format(bi, attr))

	return es


def v_prev_head_hash(blockchain):
	es = []

	for bi, block in enumerate(blockchain):
		if bi != 0:
			h = crypt.hash_block(blockchain[bi-1], attrs=["head"])
			if block["head"]["prev_block_head_hash"] != h:
				es.append("block {} prev_block_head_hash incorrect. Expected {} but found {}".format(
					bi, h, block["head"]["prev_block_head_hash"]))

	return es


def v_single_chainid(blockchain):
	chain_ids = [x["head"]["chain_id"] for x in blockchain]
	if len(list(set(chain_ids))) != 1:
		return ["Inconsistent chain IDs found: {}".format(set(chain_ids))]
	else:
		return []


def v_merkle_trees(blockchain):
	es = []

	for bi, block in enumerate(blockchain):
		if bi > 0:
			if not v_merkle(block["head"]["file_merkle"]):
				es.append("File merkle tree inncorrect for block {}".format(bi))
			if not v_merkle(block["head"]["chunk_merkle"]):
				es.append("Chunk merkle tree inncorrect for block {}".format(bi))

	return es


def v_merkle(t_merkle):
	v_merkle = merkle([t_merkle[-1]])
	return v_merkle == t_merkle


if __name__ == "__main__":
	with open(sys.argv[1]) as f:
		blockchain = json.loads(f.read())

	print("Full blockchain:")
	for x in validate_blockchain(blockchain):
		print("    {}".format(x))
	
	print("Headders only:")
	for x in validate_headders(blockchain):
		print("    {}".format(x))