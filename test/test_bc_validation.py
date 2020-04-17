import sys, os
import json
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from miner.miner import Miner
from utils.validator import validate_headers
from utils.config import Config



def test_bc_headers_valid():
	"""
	Tests a valid blockchain
	"""
	with open(os.path.join(Config.test_data_dir, "bc_headers_v.json")) as f:
		bc = json.loads(f.read())
	assert len(validate_headers(bc)) == 0, "test failed"


def test_bc_headers_invalid():
	"""
	Tests a series of invalid blockchains
	"""
	for i in range(2):
		fpath = os.path.join(Config.test_data_dir, "bc_headers_iv_{}.json".format(i))
		with open(fpath) as f:
			bc = json.loads(f.read())
		assert len(validate_headers(bc)) > 0, "test failed"



if __name__ == "__main__":
	test_bc_headers()
	test_bc_headers_invalid()