import os
from os import listdir
from os.path import isfile, join
import random
from utils.config import Config
from utils.file_encoder import encode
from utils.crypt import get_rand_str


data_dir = Config.sample_data_dir


def gen_sample_data(num_items=1, rand_str=False, size=64):
	if rand_str:
		return [get_rand_str(size=size) for x in range(num_items)]
	else:
		data = []
		sample_files = [join(data_dir,f) for f in listdir(data_dir) if isfile(join(data_dir, f))]

		if num_items > len(sample_files):
			print("WARNING: There are not enough different sample items in the sample data directory for the number requested ({}), only {} will be generated.".format(num_items, len(sample_files)))

		for i in range(num_items):
			item = {}
			fp = sample_files.pop(random.randint(0, len(sample_files)-1))
			item["data"] = encode(fp)
			item["filesize"] = os.path.getsize(fp)
			item["filename"] = os.path.basename(fp)

			data.append(item)

		return data