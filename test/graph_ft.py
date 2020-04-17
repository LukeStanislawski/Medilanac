import sys, os
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from utils.config import Config
import json
import matplotlib.pyplot as plt


def main():
	"""
	Displays a graph showing data related to average network fault tolerance
	"""
	# Load results data
	with open(Config.ft_res_file) as f:
		lines = f.readlines()

	results = []
	for line in lines:
		results.append(json.loads(line))


	# Format results data
	d_rdnds = sorted(list(set([x["d_redundancy"] for x in results])))
	avg_drd = []
	for drd in d_rdnds:
		rel = [x for x in results if x["d_redundancy"] == drd]
		frs = [x["rem_when_fail"] for x in rel]
		# avg_fr = sum(frs) / float(len(frs))
		avg_fr = 100 - ( (sum(frs) / float(len(frs))) * 100.0 / float(rel[0]["num_alt_miners"]) )
		avg_drd.append(avg_fr)

	d_rdnds = [(x-1) * 100 for x in d_rdnds]
	print(d_rdnds)
	print(avg_drd)


	# Plot data and display graph
	plt.title('Fault tolerance against data redundancy')
	plt.ylabel('Average Fault tolerance (%)')
	plt.xlabel('Data redundancy (%)')
	plt.plot(d_rdnds, avg_drd)
	plt.show()



if __name__ == "__main__":
	main()
