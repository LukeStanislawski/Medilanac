import sys, os


class Config():
	def __init__(self):
		# Main
		# ----

		# Number of miners to create
		self.num_miners = 5

		# Number of blocks each miner should generate (excluding genesis)
		self.num_blocks = 5

		# Number of foreign chunks added to each block
		self.num_foreign_chunks = 8

		# Path to blockchain dir
		self.blockchain_dir = os.path.join(
			os.path.dirname(os.path.dirname(__file__)), 
			"data", "blockchain")

		self.test_data_dir = os.path.join(
			os.path.dirname(os.path.dirname(__file__)),
			"test", "test_data")


		# Exchange
		# --------

		# Exchange internal IP address
		self.exchange_ip = "localhost"
		self.exchange_port = 5000

		# Index of chunk submittion and retrieval
		self.exchange_submit_index = "/submit"
		self.exchange_rerieve_index = "/retrieve"
		self.exchange_submit_miner = "/submit-miner"
		self.exchange_get_miners = "/get-miners"


		# Exchange public address (address miners can reach server on)
		# exchange_pub_addr = "http://64e82222.ngrok.io"
		self.exchange_pub_addr = "http://{}:{}".format(self.exchange_ip, self.exchange_port)
		self.chunk_sub_addr = self.exchange_pub_addr + self.exchange_submit_index
		self.chunk_ret_addr = self.exchange_pub_addr + self.exchange_rerieve_index
		self.miner_sub_addr = self.exchange_pub_addr + self.exchange_submit_miner
		self.get_miners_addr = self.exchange_pub_addr + self.exchange_get_miners


		# Miner
		# -----
		# TODO: Correct spelling of timeout

		# Number of attempts to submit block to the server before timeout
		self.chunk_sub_timout = 3

		# Number of attempts to submit miner existence to the server before timeout
		self.miner_exist_timout = 3

		# Number of attempts to submit miner existence to the server before timeout
		self.retrieve_miners_timout = 3

		#Wait time between attempts (seconds)
		self.miner_wait = 0.25

		# Number of attempts to retrieve foreign chunks from the server before timeout
		self.foreign_chunk_timout = 3

		# Max size of chunk to split block into
		self.max_chunk_size = 100

		# Erasure code k value: min number of chunk required to be able to reconstruct data
		self.ec_k = 4

		# Erasure code m value: total number of chunks to split data into
		self.ec_m = 5

		# Number of files/stings to add as data in each block
		self.data_items_per_block = 4

		# Directory containing sample data to be added to blockchain
		self.sample_data_dir = "data/sample_data"

		# Miner server internal IP address/domain
		self.miner_server_ip = "localhost"



		# Validation 
		# ----------

		# Number of files to validate from each block
		self.fpb = 1

		# Number of blocks to validate files from
		self.bpbc = 1


	def validate(self):
		errors = []
		warnings = []

		if self.fpb > self.data_items_per_block:
			errors.append("fpb cannot be greater data_items_per_block")


		if len(warnings) > 0:
			print("\nWARNINGS:")
			for x in warnings:
				print(" - {}".format(x))
			print("\n")

		if len(errors) > 0:
			print("\nERRORS:")
			for x in errors:
				print(" - {}".format(x))
			sys.exit()