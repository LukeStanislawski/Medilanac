import sys, os
from miner import Miner
from multiprocessing import Process


def main():
    for i in range(6):
        p = Process(target=Miner)
        p.start()


if __name__ == "__main__":
    main()