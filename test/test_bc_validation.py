import sys, os
import json
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from miner.miner import Miner
from utils.validator import validate_headders
from utils.config import Config


def test_bc_headers_valid():
	with open(os.path.join(Config.test_data_dir, "bc_headders_v.json")) as f:
		bc = json.loads(f.read())
	assert len(validate_headders(bc)) == 0, "test failed"


def test_bc_headers_invalid():
	for i in range(2):
		fpath = os.path.join(Config.test_data_dir, "bc_headders_iv_{}.json".format(i))
	with open(fpath) as f:
		bc = json.loads(f.read())
	assert len(validate_headders(bc)) > 0, "test failed"

# test_bc_headers()