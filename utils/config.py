import sys, os


class Config():
	# Main
	# ----

	# Number of miners to create
	num_miners = 50

	# Number of blocks each miner should generate (excluding genesis)
	num_blocks = 6

	# Number of foreign chunks added to each block
	num_foreign_chunks = 11

	# Erasure code k value: min number of chunk required to be able to reconstruct data
	ec_k = 9

	# Erasure code m value: total number of chunks to split data into
	ec_m = 10

	# Path to blockchain dir
	blockchain_dir = os.path.join(
		os.path.dirname(os.path.dirname(__file__)), 
		"data", "blockchain")

	test_data_dir = os.path.join(
		os.path.dirname(os.path.dirname(__file__)),
		"test", "test_data")


	# Exchange
	# --------

	# Exchange internal IP address
	exchange_ip = "localhost"
	exchange_port = 4999

	# Index of chunk submittion and retrieval
	exchange_submit_index = "/submit"
	exchange_rerieve_index = "/retrieve"
	exchange_submit_miner = "/submit-miner"
	exchange_get_miners = "/get-miners"


	# Exchange public address (address miners can reach server on)
	# exchange_pub_addr = "http://64e82222.ngrok.io"
	exchange_pub_addr = "http://{}:{}".format(exchange_ip, exchange_port)
	chunk_sub_addr = exchange_pub_addr + exchange_submit_index
	chunk_ret_addr = exchange_pub_addr + exchange_rerieve_index
	miner_sub_addr = exchange_pub_addr + exchange_submit_miner
	get_miners_addr = exchange_pub_addr + exchange_get_miners


	# Miner
	# -----
	# TODO: Correct spelling of timeout

	# Number of attempts to submit block to the server before timeout
	chunk_sub_timout = 3

	# Number of attempts to submit miner existence to the server before timeout
	miner_exist_timout = 3

	# Number of attempts to submit miner existence to the server before timeout
	retrieve_miners_timout = 8

	#Min wait time between http request attempts (seconds)
	miner_min_wait = 0.1

	#Max wait time between http request attempts (seconds)
	miner_max_wait = 0.3

	# Wait time between requesting miners list from exchange
	miner_exchange_wait = 0.5

	# Number of attempts to retrieve foreign chunks from the server before timeout
	foreign_chunk_timout = 6

	# Max size of chunk to split block into
	max_chunk_size = 100

	# Number of files/stings to add as data in each block
	data_items_per_block = 4

	# Directory containing sample data to be added to blockchain
	sample_data_dir = "data/sample_data"

	# Miner server internal IP address/domain
	miner_server_ip = "localhost"

	# Display http requests recieved by miner server
	display_http = False


	# Test
	# ----

	ft_res_file = os.path.join(test_data_dir, "ft_results.csv")


	# Config Validation 
	# -----------------

	# Number of files to validate from each block
	fpb = 1

	# Number of blocks to validate files from
	bpbc = 1

	@staticmethod
	def validate():
		errors = []
		warnings = []

		if Config.fpb > Config.data_items_per_block:
			errors.append("fpb cannot be greater data_items_per_block")

		if Config.ec_k > Config.ec_m:
			errors.append("k value must be less than m value for erasure coding")


		if len(warnings) > 0:
			print("\nWARNINGS:")
			for x in warnings:
				print(" - {}".format(x))
			print("\n")
		else:
			print("No warnings from config validation")


		if len(errors) > 0:
			print("\nERRORS:")
			for x in errors:
				print(" - {}".format(x))
			sys.exit()
		else:
			print("No errors from config validation")
