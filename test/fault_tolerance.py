import sys, os
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from reconstruct import reconstruct
from utils.config import Config
import random
import shutil
import json


def test(subject_id, k=Config.ec_k, m=Config.ec_m):
	
	print("Subject: {}".format(subject_id))
	res = {}
	res["k"] = k
	res["m"] = m
	res["d_redundancy"] = float(m) / float(k)

	bc_ids = os.listdir(Config.blockchain_dir)
	bc_ids = [x for x in bc_ids if not x.startswith(".")]
	bc_ids = [x for x in bc_ids if x != subject_id]
	
	res["num_miners"] = len(bc_ids)
	res["subject"] = subject_id
	res["num_alt_miners"] = len(bc_ids)
	res["removed_branches"] = []
	

	failed = False
	while (not failed) and (len(bc_ids) > 1):
		print(str(failed) + " - " + str(bc_ids))
		rem_sub = random.randint(0, len(bc_ids) - 1)
		rem_sub = bc_ids.pop(rem_sub)
		mv(rem_sub)
		res["removed_branches"].append(rem_sub)

		try:
			reconstruct(subject_id, buf=2)
			print("Successfully reconstructed branch")
		except Exception as e:
			print(str(e))
			failed = True
			print("Failed to reconstruct branch")


	res["rem_when_fail"] = len(bc_ids)
	move_back()

	print(res)
	return res


def mv(id):
	src = os.path.join(Config.blockchain_dir, id)
	dest = os.path.join(Config.test_data_dir, "tmp", id)
	shutil.move(src, dest)


def move_back():
	ids = os.listdir(os.path.join(Config.test_data_dir, "tmp"))
	for id in ids:
		src = os.path.join(Config.test_data_dir, "tmp", id)
		dest = os.path.join(Config.blockchain_dir, id)
		shutil.move(src, dest)


def main():
	results = []
	bcs = os.listdir(Config.blockchain_dir)
	bcs = [x for x in bcs if not x.startswith(".")]
	while len(bcs) > 20:
		bcs.pop(random.randint(0, len(bcs)-1))

	for bc in bcs:
		results.append(test(bc))

	frs = [x["rem_when_fail"] for x in results]
	avg_fr = sum(frs) / float(len(frs))
	print("Avg remaining when fail: {}".format(avg_fr))

	with open(Config.ft_res_file, "a") as f:
		for r in results:
			f.write(json.dumps(r) + "\n")


if __name__ == "__main__":
	main()