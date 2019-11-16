import sys, os



# Main
# ----

# Number of miners to create
num_miners = 1

# Number of blocks each miner should generate (excluding genesis)
num_blocks = 1

# Path to blockchain dir
blockchain_dir = os.path.join(os.path.dirname(__file__), "data", "blockchain")


# Exchange
# --------

# Exchange IP address
exchange_ip = "127.0.0.1"
exchange_port = 5000

# Used internally, edit IP and port above
exchange_addr = "http://{}:{}".format(exchange_ip, exchange_port)


# Miner
# -----

# Number of attempts to submit block to the server befiore timeout
block_sub_timout = 3

#Wait time between attempts (seconds)
miner_wait = 1
