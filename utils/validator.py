import json
from utils import crypt


def validate_headders(blockchain):
	if not v_prev_hash(blockchain):
		return False

	if not v_prev_head_hash(blockchain):
		return False

	return True


def v_prev_hash(blockchain):
	for bi, block in enumerate(blockchain):
		if bi != 0:
			h = crypt.hash_block(blockchain[bi-1])
			if block["head"]["prev_block_hash"] != h:
				return False
	return True


def v_prev_head_hash(blockchain):
	for bi, block in enumerate(blockchain):
		if bi != 0:
			h = crypt.hash_block(blockchain[bi-1], attrs=["head"])
			if block["head"]["prev_block_head_hash"] != h:
				return False

	return True
