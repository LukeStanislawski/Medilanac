import sys, os
from miner.miner import Miner
from multiprocessing import Process
from utils.config import Config


def main():
    Config.validate()

    for i in range(Config.num_miners):
        p = Process(target=Miner, args=[i, i+5001])
        p.start()


if __name__ == "__main__":
    main()