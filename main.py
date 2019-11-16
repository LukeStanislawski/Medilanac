import sys, os
from miner import Miner
from multiprocessing import Process
import config


def main():
    for i in range(config.num_miners):
        p = Process(target=Miner)
        p.start()


if __name__ == "__main__":
    main()