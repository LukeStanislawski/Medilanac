import sys, os



# Main
# ----

# Number of miners to create
num_miners = 3

# Number of blocks each miner should generate (excluding genesis)
num_blocks = 3

# Number of foreign chunks added to each block
num_foreign_chunks = 8

# Path to blockchain dir
blockchain_dir = os.path.join(
	os.path.dirname(os.path.dirname(__file__)), 
	"data", "blockchain")


# Exchange
# --------

# Exchange internal IP address
exchange_ip = "localhost"
exchange_port = 5000

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
retrieve_miners_timout = 3

#Wait time between attempts (seconds)
miner_wait = 0.25

# Number of attempts to retrieve foreign chunks from the server before timeout
foreign_chunk_timout = 3

# Max size of chunk to split block into
max_chunk_size = 100

# Erasure code k value: min number of chunk required to be able to reconstruct data
ec_k = 4

# Erasure code m value: total number of chunks to split data into
ec_m = 5

# Directory containing sample data to be added to blockchain
sample_data_dir = "data/sample_data"

# Miner server internal IP address/domain
miner_server_ip = "localhost"