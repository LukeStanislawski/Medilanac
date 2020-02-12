# Medilanac

Author: Luke Stanislawski

email: psyls6@nottingham.edu.cn

## Current Status of Project

This project is still in development, the main current functionalities of the project are as follows:

 - Currently multiple miners are adding randomly generated ascii data to blocks on their own chains in parrallel
 - Each block is split into erasure code chunks and sent to an exchange
 - Foreign chunks are downloaded from the exchange and added to each block before publishing the block to it's blockchain
 - Data from a chain can be reconstructed from blocks on other chains
- Files can be converted to base64 and then stored as ascii on the blockchain


### TODO

- Blockchain query functionality
- Blockchain validation when accepting foreign chunks


## Installation

### Prerequisites

You are required to have [Anaconda Python](https://www.anaconda.com/) installed on your machine. Please note that medilanac has only been tested on Mac OSX.

### Creating a New Environment

The following commands will create a new conda enviroment running the required version of Python (3.7):

```
conda create -n medilanac python=3.7
conda activate medilanac
```

### Installing Dependencies

The following commands will install all the necessary Python libraries. Please execute them in the order given, answering 'y' when prompted:

```
pip install zfec
conda install pycrypto=2.6.1 flask=1.1.1 urllib3=1.25.6
```

## Running the software

**1. Running the exchange:**

First we need to launch the exchange, a simple web server that will run locally on your machine allowing different miners to exchange chunks of their blocks. 

Run the following command from inside the main project folder:

```
python exchange.py
```


**2. Run the miners:**

Next we will run the miners. The program will create multiple miner processes all generating and exchanging chunks between eachother via the exchange. They will all write their blockchains as they are being generated to their respective folders in the `data/blockchain` directory within the project folder.

Open a new terminal window, activate your environment, and run the following command from inside the main project folder:

```
python main.py
```

**3. Reconstructing a chain:**

Copy the chain ID from the folder of the blockchain you wish to reconstruct and then move the folder to somewhere else on your machine so that we know it is not being used to reconstruct the blockchain.

Run the following command from inside the main project folder replacing `<chain_id>` with the ID (or first 8 charachters of the ID of the chain you wish to reconstruct:

```
python reconstruct.py <chain_id>
```

The script will create a new blockchain in the blockchain directory with the original blockchain (excluding the foreign chunks).

## Dependencies

The following dependencies are required to run the software and can be installed by following the installation instructions:

- Python 3.7.5
- pycrypto 2.6.1
- flask 1.1.1
- urllib3 1.25.6
- zfec 1.5.3