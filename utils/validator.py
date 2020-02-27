import json
from utils import crypt
from utils.merkle import merkle


def validate_headders(blockchain):
	if not v_prev_head_hash(blockchain):
		return False
	if not v_single_chainid(blockchain):
		return False
	if not v_merkle_trees(blockchain):
		return False


	return True


def v_prev_head_hash(blockchain):
	for bi, block in enumerate(blockchain):
		if bi != 0:
			h = crypt.hash_block(blockchain[bi-1], attrs=["head"])
			if block["head"]["prev_block_head_hash"] != h:
				return False

	return True


def v_single_chainid(blockchain):
	return len(list(set([x["head"]["chain_id"] for x in blockchain]))) == 1


def v_merkle_trees(blockchain):
	for bi, block in enumerate(blockchain):
		if bi > 0:
			if not v_merkle(block["head"]["file_merkle"]):
				return False
			if not v_merkle(block["head"]["chunk_merkle"]):
				return False

	return True


def v_merkle(t_merkle):
	v_merkle = merkle([t_merkle[-1]])
	return v_merkle == t_merkle
