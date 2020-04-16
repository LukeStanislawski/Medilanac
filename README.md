# Medilanac

Author: Luke Stanislawski

email: psyls6@nottingham.ac.uk

## Current Status of Project

The main current functionalities of the project are as follows:

- Currently multiple miners are adding files in the form of ascii text to blocks on their own chains in parrallel
- Each miner announces their existence and the network address that they can be reached at to an exchange server
- Each block generated is split into erasure code chunks
- Miners download foreign chunks directly from other miners on the network and add to each block before writing the block to it's blockchain
- Data from a chain can be reconstructed from chunks in blocks on other chains
- Files can be converted from base64 ascii and reconstructed


## Installation

### Prerequisites

You are required to have [Anaconda Python](https://www.anaconda.com/) installed on your machine. Please note that Medilanac has only been tested on OSX 10.15.4.

### Creating a New Environment

The following commands will create a new conda enviroment running the required version of Python (3.7):

```
$ conda create -n medilanac python=3.7
$ conda activate medilanac
```

### Installing Dependencies

The following commands will install all the necessary Python libraries. Please execute them in the order given, entering 'y' if prompted:

```
$ pip install zfec pytest
$ conda install pycrypto=2.6.1 flask=1.1.1 urllib3=1.25.6 numpy
```

## Running the software

**1. Running the exchange:**

First we need to launch the exchange, a simple web server that will run locally on your machine allowing different miners to exchange chunks of their blocks. 

Open a terminal window, activate the medilanac python environment, and run the following command from inside the main project folder:

```
$ python exchange.py
```


**2. Run the miners:**

Next we will run the miners. The program will create multiple miner processes all generating blocks and exchanging chunks between each other. They will all write their blockchains as they are being generated to their respective folders in the `data/blockchain` directory within the project folder.

Open a new terminal window, activate the medilanac python environment again, and run the following command from inside the main project folder:

```
$ python main.py
```

**3. Reconstructing a chain:**

Copy the chain ID from the folder of the blockchain you wish to reconstruct and then move the folder to somewhere else on your machine so that we know it is not being used to reconstruct the blockchain (this is not strictly necessary as the reconstruction script only loads foreign chunks and ignores all primary data on branches).

Run the following command from inside the main project folder replacing `<chain_id>` with the ID (or first 8 charachters of the ID of the chain you wish to reconstruct:

```
$ python reconstruct.py <chain_id>
```

The script will create a new blockchain in the blockchain directory with the original blockchain (excluding the foreign chunks).

**Adjusting Parameters**

All parameters for the simulation can be adjusted by changing the values in `utils/config.py`. The config parameters are validated when the software initiates.

## Testing

The tests can be run using pytest with the following command from inside the project directory:

```
$ py.test
```

To run an end-to-end test of the system, enter the following command:

```
$ py.test test/test_e2e.py
```

## Dependencies

The following dependencies are required to run the software and can be installed by following the installation instructions:

- Python 3.7.5
- pycrypto 2.6.1
- flask 1.1.1
- urllib3 1.25.6
- zfec 1.5.3
- pytest 5.3.5