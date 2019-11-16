# Final Year Project

Author: Luke Stanislawski

email: psyls6@nottingham.edu.cn

## Current Status of Project

 - Currently multiple miners are adding random ascii data to blocks on their own chain in parrallel.
 - Block is split into chunks and sent to an exchange


## Prerequisites

The following software is required:

- Python 3.7.5
- pycrypto 2.6.1
- flask 1.1.1


## Running the software

*To run the exchange:*

Run the following command from inside the main project folder:

```
python exchange.py
```


*To run the miners*

Run the following command from inside the main project folder:

```
python main.py
```