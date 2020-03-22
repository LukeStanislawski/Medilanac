import sys, os
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from reconstruct import reconstruct
from utils.config import Config
import random
import shutil

def main():
	res = {}
	bc_ids = os.listdir(Config.blockchain_dir)
	bc_ids = [x for x in bc_ids if not x.startswith(".")]
	res["num_miners"] = len(bc_ids)
	failed = False

	subject = random.randint(0, len(bc_ids) - 1)
	subject = bc_ids.pop(subject)
	res["subject"] = subject
	res["removed_branches"] = []

	while (not failed) and (len(bc_ids) > 1):
		print(str(failed) + " - " + str(bc_ids))
		rem_sub = random.randint(0, len(bc_ids) - 1)
		rem_sub = bc_ids.pop(rem_sub)

		rem_sub_path = os.path.join(Config.blockchain_dir, rem_sub)
		shutil.rmtree(rem_sub_path)
		res["removed_branches"].append(rem_sub)

		try:
			reconstruct(subject)
			print("Successfully reconstructed branch")
		except Exception as e:
			print(str(e))
			failed = True
			print("Failed to reconstruct branch")

		# print("---")
		# print(reconstruct(subject))


	res["rem_when_fail"] = len(bc_ids)
	print(res)



if __name__ == "__main__":
	main()