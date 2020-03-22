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
	res["num_alt_miners"] = len(bc_ids)
	res["removed_branches"] = []
	
	print("Subject: {}".format(subject))

	while (not failed) and (len(bc_ids) > 1):
		print(str(failed) + " - " + str(bc_ids))
		rem_sub = random.randint(0, len(bc_ids) - 1)
		rem_sub = bc_ids.pop(rem_sub)
		mv(rem_sub)
		res["removed_branches"].append(rem_sub)

		try:
			reconstruct(subject, buf=1)
			print("Successfully reconstructed branch")
		except Exception as e:
			print(str(e))
			failed = True
			print("Failed to reconstruct branch")


	res["rem_when_fail"] = len(bc_ids)
	print(res)

	move_back()


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



if __name__ == "__main__":
	main()