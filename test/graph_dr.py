import sys, os
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from utils.config import Config
import json
import matplotlib.pyplot as plt
import numpy as np


def main(fpath):
	"""
	Displays a graph showing data related to block data ratio
	"""
	# Load results data
	with open(fpath) as f:
		lines = f.readlines()

	results = []
	for line in lines:
		if not line.startswith("//"):
			results.append(json.loads(line))

	# Format relevent data
	results = sorted(results, key=lambda k: k['data_lens']["mean"])
	# x = [np.log(x["block_lens"]["mean"]) for x in results]
	x = [x["data_lens"]["mean"] for x in results]
	y = [x["mean"] for x in results]
	yy = [x["block_lens"]["mean"] for x in results]


	# Plot graphs
	plt.figure(figsize=(14,5))
	plt.subplot(1,2,1)
	plt.title('Ratio of Total Block Size to Primary Data Size Against Primary Data Size')
	plt.ylabel('Total Block Size / Primary Data Size')
	# plt.xlabel('log( Primary Data Size )')
	plt.xlabel('Primary Data Size (chars)')
	plt.plot(x, y)

	plt.subplot(1,2,2)
	plt.title('Total Block Size Against Primary Data Size')
	plt.ylabel('Total Block Size (chars)')
	plt.xlabel('Primary Data Size (chars)')
	plt.plot(x, yy)


	plt.show()



if __name__ == "__main__":
	if len(sys.argv) > 1:
		main(sys.argv[1])
	else:
		main(Config.dr_res_file)
