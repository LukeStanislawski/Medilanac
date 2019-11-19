# Medichain

Author: Luke Stanislawski

email: psyls6@nottingham.edu.cn

## Current Status of Project

This project is still in development, the main current functionalities of the project are as follows:

 - Currently multiple miners are adding randomly generated ascii data to blocks on their own chains in parrallel
 - Each block is split into erasure code chunks and sent to an exchange
 - Foreign chunks are downloaded from the exchange and added to each block before publishing the block to it's blockchain

### TODO

- Data reconstruction functionaity
- Blockchain query functionality
- Blockchain validation when accepting foreign chunks
- Store non-ascii data


## Installation

### Prerequisites

You are required to have [Anaconda Python](https://www.anaconda.com/) installed on your machine. Please note that Medichain has only been tested on Mac OSX.

### Creating a New Environment

The following commands will create a new conda enviroment running the required version of Python (3.7):

```
conda create -n medichain python=3.7
conda activate medichain
```

### Installing Dependencies

The following commands will install all the necessary Python libraries. Please execute them in the order given, answering 'y' when prompted:

```
pip install zfec
conda install pycrypto=2.6.1 flask=1.1.1 urllib3=1.25.6
```

## Running the software

**To run the exchange:**

Run the following command from inside the main project folder:

```
python exchange.py
```


**To run the miners:**

Run the following command from inside the main project folder:

```
python main.py
```

## Dependencies

The following software is rewquired to run:

- Python 3.7.5
- pycrypto 2.6.1
- flask 1.1.1
- urllib3 1.25.6
- zfec 1.5.3