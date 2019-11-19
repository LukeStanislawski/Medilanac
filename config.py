import sys, os



# Main
# ----

# Number of miners to create
num_miners = 3

# Number of blocks each miner should generate (excluding genesis)
num_blocks = 2

# Path to blockchain dir
blockchain_dir = os.path.join(os.path.dirname(__file__), "data", "blockchain")


# Exchange
# --------

# Exchange IP address
exchange_ip = "127.0.0.1"
exchange_port = 5000

# Index of chunk submittion and retrieval
exchange_submit_index = "/submit"
exchange_rerieve_index = "/retrieve"


# Used internally, edit IP and port above
exchange_addr = "http://{}:{}".format(exchange_ip, exchange_port)
chunk_sub_addr = exchange_addr + exchange_submit_index
chunk_ret_addr = exchange_addr + exchange_rerieve_index


# Miner
# -----

# Number of attempts to submit block to the server before timeout
chunk_sub_timout = 3

#Wait time between attempts (seconds)
miner_wait = 1

# Number of attempts to retrieve foreign chunks from the server before timeout
foreign_chunk_timout = 3

# Max size of chunk to split block into
max_chunk_size = 100

# Number of foreign chunks added to each block
num_foreign_chunks = 3

# Erasure code k value: min number of chunk required to be able to reconstruct data
ec_k = 4

# Erasure code m value: total number of chunks to split data into
ec_m = 5