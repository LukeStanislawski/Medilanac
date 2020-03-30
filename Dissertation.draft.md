# Interim Report

## Abstract

Medical data of an individual is commonly stored in a fragmented manner in many different locations which restricts ease of retrieval by patients and the collation of large useful datasets by researchers. Furthermore, studies have shown that patients benefit from a clear holistic view of their medical data [9]. Blockchain has the potential to free up medical data, advancing research and improving the healthcare delivery. At the same time blockchain technology enhances patient privacy and security. Medilanac is a blockchain networking design which, unlike other similar implementations, stores medical data on the blockchain itself. Our design, the Medilanac, proposes a new protocol to overcome the inherent inefficiencies of storing large datasets on the blockchain posed by the technology itself. Therefore maintaining the data validation and recovery functionality of standard blockchain technology, and at the same time allowing for the storage of large and diverse data sets.

## Background and Motivation

The increase in data harvesting and storage in recent years has led to an increase in the widespread development of artificial intelligence systems for statistical analysis and pattern recognition on large datasets for the purpose of improving healthcare. Consequentially, conversations about the trade off between advancements in medical research and the right to privacy of the individual have become mainstream [3]. 

For many medical professionals, their skills development and consequently their contributions to healthcare are inhibited by a lack of accurate and timely feedback [1]. AI systems do not suffer from such a problem. With large datasets, AI systems facilitate data analysis that can divulge complex patterns linking specific practices/decisions undertaken during treatment of individuals, with significant outcomes and degrees of success that would otherwise not be elucidated. Newly discovered practices can then be adopted, improving healthcare [4]. They are able to examine, in detail, orders of magnitude more medical records than human doctors can in their finite careers, learning and improving from each one, allowing them to give more accurate diagnoses and recommendations for treatment. 

A decentralized, international medical database which is available to all could facilitate significant improvements in medical practices. The ability to compare the short-term and long-term outcomes of treatments performed in different locations around the world, would facillitate analysis of the strengths and weaknesses of diverse practices, and serve as a major catalyst for improvement [5]. Providing patients with a clearer view of their complete medical records would also offer more immediate benefit [9].

## Literature Review

Many attempts have been made to combine medical data and blockchain technology. However, none has managed to find a solution to the inherent problem with blockchain which is that it is poorly suited to storing large amounts of data [2]. This is because every user (node) on the network must have a complete copy of the entire blockchain.

As the blockchian is an *append only* data structure, if we were to merely create a protocol that allowed for medical data to be stored on a standard blockchain, it is likely that it would either quickly grow to an unmanageable size or would not be able to store adequate amounts of data in a timely manner; From Q3 2018 to Q3 2019, Bitcoin, the most prominent cryptocurrency built on top of a blockchain, saw its blockchain size increase by 57.764 GB to a total of 242 GB, from an estimated 5.8 million active users [6,7]. We can therefore calculate that the average annual blockchain data contribution is approximately 10 KB per person per year. Consequently, if someone wants to store and retrieve the annual transaction data of say 5000 people, amounting to 50 MB, they must store the entire 242GB blockchain, some 4840 times more data than that of which they desire. When considering a typical small GP clinic hoping to store the medical records of its 5000 registered patients on a system equivalent in design to bitcoin but repurposed for the storage of medical data, the problem is clear [26].

### Blockchain

Blockchain was originally conceptualised by an individual acting under the alias of 'Satoshi Nakamoto' for the purpose of creating a decentralised trust-less peer-to-peer cash system [2]. Their paper proposes a public ledger that is append-only and completely immutable. That is, once something has been added to the ledger and accepted by the majority of the rest of the network, it is nearly impossible to change it. To do so would require cooperation of at least 51% of the computing power on the network, something that the protocol relies on being unachievable for the security of the network.

The protocol hosts an ongoing open competition pitting contestants(*miners*) against each other, all attempting to be the first to solve a computationally laborious maths puzzle. The winner is able to publish the next block (containing users data) on to the blockchain and receive their reward for doing so. The maths puzzle is such that it is difficult to find the answer, but easy to verify the correct one. Therefore once any given miner successfully finds the answer to the next block, all other nodes can quickly verify it and begin working on finding the solution to the subsequent block.

![](Diss.assets/Blockchain_nb.png)

The majority of the data within each block is data submitted by the end users to the miners for publishing. This data must also meet a set of criteria that all of the miners agree to. If the data does not meet the accepted criteria, it will be invalid and will not be accepted onto the blockchain by the rest of the network.

#### Smart Contracts

In recent years, the most significant developments have emerged in the form of smart contracts. Blockchains such as the Ethereum blockchain allow for code written in Turing-complete languages to be added and executed on the blockchain [16]. The advent of smart contracts has meant that functionality of blockchains has moved beyond just the mere storage of data, and towards the advent of distributed computing [21, 22]. It is now possible to execute complex and immutable programs in predefined, predictable ways. Untrusting parties are therefore able to cooperate in ever increasing amounts, whilst maintaining assurance against security breaches.

#### Blockchain Sharding

Zamani et al introduced a method of sharding a blockchain such that minimal node inter-shard validation is required [20]. Validation is carried out by a *committee* of nodes elected for each *epoch*. The committee of each shard is responsible for communicating with the committee of other shards in order to validate data on their own shard for which the process of validation requires data on a different shard. Minimal validation is undertaken by the majority of nodes on the network, and very few of them are required to process data from other shards with each *epoch*.

### Erasure Coding

Data redundancy is an inevitability when ensuring reliability in a network [18]. Erasure coding is a way of maximising the reliability whilst minimising the data redundancy required to achieve it. The encoding algorithm is a method of protecting data $d_{o}$ from corruption/loss by splitting the data into $k$ *fragments* ($ f_{i}, i = 1..k-1$) and then encoding those fragments into *chunks* $c_{i}, i = 0..m-1$, such that the original data can be recovered with any number $k, k<m$ of the chunks [14]. Each of the encoded chunks is one of the linear combinations of the fragments of $d_{o}$. The summation of size of all encoded fragments is greater than the size of the original data, $ \sum_{i=0}^{m-1}size(c_{i}) > size(d_{o})$; hence the aforementioned inevitable redundancy.

The Medilanac system uses erasure coding as a method of mitigating the risk of failure to reconstruct a block on the network as a result of data loss. We will do this by requiring every block that is added to the network to be encoded into $m$ chunks using erasure coding. These chunks will then be stored on various different branches on the network.

#### Blockchain and Erasure Coding

> TODO: Intro here

Perard et al propose the idea of a Low Storage Node on a blockchain [17]. Their system design incorporates erasure coding such that nodes need not store a copy of each entire block, but merely a single chunk of data from each. Greatly reducing the amount of data each node is required to store. Their system is designed to be more accommodating to nodes with less storage capacity but is not equipped to deal with a the heavy data requirements of medical data on a large scale. Furthermore, the network requires miners to compete to add blocks to the network. This is a hugely inefficient design as it requires significant infrastructure and electricity to maintain. A study from The University of Cambridge found that Bitcoin's annual energy consumption is roughly in line with that of Switzerland [23, 24]. These are costs that are ultimately passed onto the patients.

Furthermore, their solution In forcing all nodes to store the same (reduced) amount of data and is therefore not suitable for the storage of medical data as it fails to handle the inevitability of some nodes producing more data than others. With no motivation to moderately add data to the network, a 'tragedy of the commons' situation emerges such that the size of the blockchain would rapidly explode and become unusable.

### Blockchain In Medical Data

#### MedRec

One of the most notable current implementations combining blockchain and the storage of medical data is that of MedRec, a Medical record storage system built to work on top of the Ethereum blockchain [8]. The system uses smart contracts to manage the permissions of medical record viewership, incentivising miners with the reward of anonymised medical data that can be used for research. The medical data itself is stored on healthcare providers databases who allow anyone who has the permission of the owner (according to the blockchain) to view or update the medical records.

MedRec gives users a comprehensive and holistic view of when and by whom their medical data has been changed, which benefits patients [9]. Privacy concerns are combatted with transparency by allowing patients to more easily see what information can be derived from their complete set of medical data. Patients can therefore be more confident that their data is unlikely to exist anywhere else such that it could be aggregated, allowing for more information to be derived without their knowledge.

The greatest weakness of this approach are that the individuals must still trust their service providers to offer a *good* service. Individuals must trust that the provider will sufficiently backup and manage their databases, so that their data will not be lost. If the data itself is lost then the provider would not be capable of retrieving it for the patient and the smart contract on the blockchain would become void. Patients are required to trust that the provider will implement adequate security measures to their databases in order to prevent their medical data being stolen and their privacy breached. Similarly, they must also trust that the provider will not sell or share their data without the permission of the patient, no guarantee of which is given by the permissions of the blockchain. Finally the patient is required to trust that the provider will not withhold the data from the patient or any authorised party. It is easy to assume that the business model of the provider would incorporate some assurances in relation to these issues, however business decisions are often overruled by governments or other subjective motivations.

#### e-Estonia

Many similar system designs have been proposed by others, all of which require data to be stored off-chain, and only access rights to be stored on-chain [10, 11]. One such system is that of the KSI blockchain system used for the Estonian "e-Estonia" initiative [19]. The national blockchain system stores data and backups on servers in a conventional manner. The blockchain is then combined with a time-stamping server to ensure authenticity and time of permissions. This system is therefore predominantly centralised; the government has complete control over the time-stamping server, databases and blockchain itself. It is theoretically possible, therefore, for the government to edit and remove data on the blockchain, or forge a timestamp for data.

#### MedBlock

The system proposed by Fan et al proposes a distributed ledger containing only summaries or electronic medical records (EMRs), the detailed sources of which remain in the databases of health service providers [12]. The EMR summaries also contain the cryptographic hashes of the source data to ensure they are tamper-proof. However, patients must still trust the service providers to competently and ethically store the full EMRs for them, which they often do not [25], and therefore many of the same issues arise as with the MedRec system.

#### Third Party Hosting

Zyskind et al put forward a system where a data storage service is trusted with an encrypted version of the medical data, and a blockchain used for logging and permissions control [13]. The idea of encrypting data stored by the service provider offers good protection against unauthorised sharing of the data as it is of no use without the key. Therefore a system design ensuring that the party storing the patients data never possesses the key to said data eliminates this requirement of the patient to trust in the provider to not share their data without permission. However, there is no guarantee that the data storage service will not withhold or lose the (encrypted) data. Therefore the patients must still trust the provider to store their data competently and act within the confines of their agreement.

## Methodology

This project is tasked to design of an algorithm which incorporates multiple different stakeholders. As such, higher level functional requirements can be defined that apply to the system design as a whole, while lower level non-functional requirements apply only to their respective stakeholders.

### Functional Requirements

The system must satisfy all of the following requirements:

1. Data must be stored such that the data owner does not need to trust the data storer to: 
  1. Adequately protect data from loss and theft,
  3. Not share data without permission from the data owner,
  4. Not withhold data from owner.
2. Data must be able to be retrieved in a timely manner.
3. The data owner must be able to remain in control of their data.
4. The user must not be required to store an *unreasonable* amount of extra data when adding their own.
5. Publicly shared data should be in a format that facilitates large scale data mining.

### Non-functional requirements

#### Data Storage Provider (Miner)

The network protocol must ensure that all blocks added to the network conform to the following set of standards, and that blocks failing to do so are not accepted by the rest of the network:

- Each block must be signed to ensure authenticity.
- Each block must contain a number of foreign chunks such that the size of data used by the foreign chunks is equal to the size of data used by the branch's own data, plus the threshold amount.
- Blocks must be split up into chunks using erasure coding and submitted for storage on other branches.

#### Patients (Users)

- Users/patients must add data in a format the conforms to a specific schema.
- Data must be signed.
- Private data must be encrypted.

## System Design

1. Overview
   1. Users data is stored by a miner
   2. Miners store data on a permissioned blockchain
   3. Miners generate erasure coded chunks of each block
   4. Miners exchange chunks
   5. Branch reconstruction
2. Exchange and peer discovery
3. Erasure coding of blocks
4. Exchanging of chunks between miners
5. Process of reconstruction
6. Stakeholder Motivations

---

### Overview

The system design dictates that user data is stored by secondary parties referred to from here on as miners. The chosen miner will be the primary storer of the users data. This allows for the inevitability of user incompetence as the miners can be the ones who build user gateways to the network.

The miners will store user data in the form of a blockchain. The blockchain ensures that data, once added, cannot be altered by any party, without invalidating said data. Instead of a single blockchain with many miners competing against each other, the proposed system requires each miner to have their own permissive blockchain shard (branch), that is, a blockchain that can only be added to by its 'own' miner. The use of digital signatures can verify the author of a block. Furthermore, miners can do this without being required to solve any maths puzzle (proof of work). This means that every miner on the network has complete control over when they add extra nodes to their branch. As the miners are the only ones storing a full copy of their blockchain, they are also *expected* to share their entire chain with anyone who wishes to query it, although an explanation is presented later of how the network can cope with a node that does not comply.

After sourcing all of the desired data to be stored on a single block, the miner will encode the block using an erasure coding algorithm into multiple smaller fragments referred to from here on as 'chunks'. Chunks are the erasure code fragments of blocks on the network that can be reconstructed (with any number $n \geq k$) into the original block. Therefore, any party wishing to reconstruct any given block, need only require $k$ chunks. 

These chunks are then distributed out to other miners on the network. Similarly, chunks from other miners are retrieved and the validity is verified. These chunks pertaining to data on the blockchain of miners other than the subject, from here on referred to as 'foreign chunks', is added to the miners block currently being generated. In this way, data redundancy is achieved and distributed across the network, allowing for safer storage of data.



![Adding a block C4 to branch C requires the miner to add chunks from blocks in other branches to C4](Diss.assets/Adding_Block.png)

*Adding a block C4 to branch C requires the miner to also add chunks from blocks in other branches to C4.*

Resultantly, data can then be reconstructed in the event of a loss of primary branch, from chunks that are stored on other miners branches on the network. This can be easily achieved by querying other miners for chunks pertaining to a given branch, and retrieving those chunks. This capability therefore accounts for the eventuality of a malicious or incompetent miner, allowing users to reconstruct their data from other nodes on the network.

#### Miner Peer Discovery

Communication between miners is peer to peer (serverless), this is crucial in order for the network to remain decentralised. Therefore, the network must implement a mechanism for peer discovery. For the simulation, I have chosen to add an exchange to the design of the system because it is the simplest mechanism for peer discovery. The decentralised nature of the network is not affected by this design as the exchange has very little control over the network as it is only able to listen for miners announcing their presence, and return a list of all miners in existence, along with their url, when requested. No heavy data processing or validation is undertaken by the exchange, the miners must decide which other miners to trust. Additionally, if this design were to be kept in a production environment, multiple exchanges could exist, further reducing the threat of centralisation.

#### Block Erasure Coding

One of the design challenges with splitting each block up into pieces and storing them in different locations is that blockchain protocols require every single byte of a block to be present. If a single one is missing, the hash cannot be verified and the blockchain is broken. Therefore if a single chunk was lost, the entire branch from that block onwards would become invalid and could not be reconstructed. For the system to be useable, it must have a reasonable fault tolerance. We must therefore incorporate a way to allow for some chunks to be lost and still be able to reconstruct an entire block.

With each block added to their blockchain, the miner must include a number of *chunks* of blocks from the blockchains of other miners. Chunks are the erasure code fragments of blocks on the network that can be reconstructed (with any number $n \geq k$) into the original block. Data on a branch pertaining to another will from here on be referred to as *secondary* data consisting of foreign chunks. The data created/added by the miner of a blockchain will be known as *primary* data. Hence primary data on one branch is encoded into chunks and becomes secondary data on a different branch. In accepting secondary data, miners are essentially contributing to the back up of other blocks on the network. The required ratio of primary/secondary data in each block on the network is defined by the protocol, but will have to be a minimum of $(k + m) S_{p}$ where $S_{p}$ is the size of the primary data in each block. 

After adding the block, the miner must use erasure coding to encode the block's primary data into chunks, and send to other miners on the network to store on their blockchains (as foreign data). If the miner loses access to a chunk on another branch, they must replace it on a different branch in the network in order to maintain a sufficient backup on the network.

![B](Diss.assets/Block.png)

*Logical overview of the contents of each block on a blockchain.*

Without erasure coding, the miner of any given branch ($b_{i}$) storing a fragment of any block originating from another ($b_{j}$), would have the power to corrupt the backup of the corresponding block. By the very nature of blockchain, it is essential to know the value of every single bit and byte of each block, otherwise the hash of the block cannot be verified and every subsequent block becomes invalid. Erasure coding is used so that in the event of a patients losing access to a branch, whether from loss of data or from an uncooperative service provider, the primary data of a branch can be reconstructed with $k$ foreign chunks, as opposed to all $m$ fragments. Therefore, as long as a large enough proportion of the nodes storing the data ($k/m$) successfully return the data, we can reconstruct all primary data on a branch.

For the network to function correctly a certain proportion of nodes must be cooperating with the rest of the network. This proportion is hypothesised to be mathematically related to the amount of additional erasure code that is generated for each block, and the number of branches on the network. However, further investigation is required in order to confirm this hypothesis and find an exact relationship.

In distributing chunks obtained from encoding blocks using an erasure coding algorithm, the protocol introduces a certain amount of data redundancy. Therefore when attempting to reconstruct a block in the event of a miner failure, the party attempting to reconstruct the block need only obtain a fraction of all the chunks stored on the network to reconstruct the original data.

### Exchanging of Chunks

> TODO: revisit

It is in each miners interest to have *their* chunks stored on a reputable blockchain rather than an untrustworthy one. This is because the network as a whole has an average fault tolerance of nodes. This fault tolerance can be reduced for any miner storing chunks on a branch belonging to a miner that is not acting in accordance with the protocol of the network. Therefore each miner must perform some kind of verification procedure when distributing and retrieving chunks.

The structure of each block has been designed with this in mind. Each block contains a merkle tree of all primary data items and foreign chunks. This allows any miner ($A$) attempting to validate the blockchain of another miner ($B$) to first query $B$ for a summary of their blockchain. This summary comes in the form of a blockchain containing only the block headers. The block headers are only a fraction of the size of the entire block, enabling quick retrieval over finite bandwidth. $A$ can then challenge $B$ to return any specific files chosen by A. These files can be verified to be in the blockchain using the merkle tree. In this way, it is very difficult for $B$ to appear to be storing data without being able to produce fragments of it on demand. After several  sections of data that were randomly chosen by $A$ have been produced $B$, $A$ can be confident that $B$ is storing the data they claim to be.

Intuitively then, any miner attempting to use the backup capability of the network without also contributing to it by storing and serving on demand other miners data will struggle to find any other miners on the network willing to store their chunks.

### Branch Reconstruction

> TODO: revisit

Branch reconstruction can be carried out by any party at any time, however its utility is designed to allow data owners to retrieve their data in the event of a failure of a miner. Reconstruction is carried out by querying all/enough miners on the network for chunks pertaining to the specific branch that is being reconstructed. Once enough chunks for each block have been retrieved according to the redundancy threshold set out in the protocol ($k$), the block can be reconstructed using the inverse of the algorithm used to encode the block into chunks. So long as all previous blocks can also be successfully reconstructed, the block can be validated, although there are ways of mitigating this limitation that will be outlined later.

It is important to note that as only the primary data of each block is split into chunks and distributed across the network, only this data can be reconstructed. Foreign chunks of blocks cannot be reconstructed. This is because foreign chunks are backups of primary data on other branches. Requiring foreign chunks to be stored again would create a recursive storage requirement that would quickly render the network incapable of storing any  data. For this reason, miners can expect to donate an amount of storage to the network that is linearly proportional to the amount that they use. Specifically, the amount of data they use plus the redundancy rate laid out in the protocol.

### Stakeholder Motivations

Outlined below is a description of the motivations of both the miners and patients, as well as the consequences of critical actions/inactions from both.

#### Miners

Just as is commonly the case in current systems, miners are financially incentivised to store patient data on the network, either through government or private funding. However, they must also *donate* an amount of storage to the network proportional to the amount they use. Therefore they cannot spam the network with data as to do so would also require them to donate large amounts of storage to the network, a troublesome task which would ultimately negate the affects of their intentions. Miners will also need to periodically check that chunks they have stored on other branches are still accessible.

Miners have no direct incentive to release foreign data upon the request of another branch requesting. However, uncooperative nodes will eventually be discovered after enough failed requests, and will find themselves blacklisted by most other miners on the network. The network assumes that the majority of branch owners intend to work together, and can handle a certain threshold of malicious nodes. Therefore a node looking to cut costs by not handling requests from other nodes whilst resting assured that their data is sufficiently backed up, may soon find themselves *shunned* from the network.

#### Patients

Patients have the choice of which branch to select to store their data. As each branch offers a near identical service, and mobility of data is high, service prices will remain competitive. Many branches will offer incentives such as discounts in return for de-anonymisation of certain medical information which could be used for research. Governments may set up multiple branches and provide the service for free. Either way, the choice remains with the patient.

All patient data uploaded to the network will be visible to all parties; this is required in order to validate the data with regards to the hashes on the blockchain. Therefore patients will be required to encrypt any private medical data. Patients will be able to easily upload any data to the network unencrypted or share read-only keys with specific parties should they wish to donate personal data for research purposes.

### Implementation Dependent Alternatives

> TODO: Write up. Possibly move section to implementation.

- Miners query specific block headers
- Block size
- Fragmentation of files on block such that each merkle tree leaf is for a fixed size of memory.
- Blocks store hashes of previous 2/3 blocks instead of just 1 allowing for the failure of one block
- Each block is its own json file, maybe also headers etc
- Hash linking blocks does not include primary or foreign data, only merkle trees of both

## Implementation

The implementation of the Medilanac network protocol consists of a simulation of the different components and stakeholders of the network. The system will incorporate all of the relevant security features to make it as robust as a deployable version of the network would be. The simulation will be able to span across multiple different machines on multiple different networks. This is important as the original algorithm will most likely be implemented on top of the TCP/IP layer of the Internet. Therefore a working simulation that incorporates the technologies that already exist offers a stronger proof of implementability.

Currently the system has some security features in place such as the hashes linking blocks together, and digital signatures of chunks published to the exchange. However, the system is still insecure and does not adequately represent the level of security required.

### Modules

The blockchain generation module will consist of simulated miners, a data exchange and a data reconstruction script. The miners simulate the role of the branch owners in building and signing the blockchain. The exchange facilitates the communication of the different miners, sharing chunks between branches. The reconstruction script serves as a demonstration of the algorithm that patients would follow if they were to lose access to the branch containing their data.

#### Miners

The miners run on different processes on the computer with no shared memory and hence all communications go through the exchange. The miners generate data that symbolises the medical records being added to the network by patients, which are then used to generate a block. A copy of the block is encoded into chunks using the Reed Solomon Erasure Coding protocol, these chunks are then published to the exchange.

#### Exchange

The exchange serves the purpose of receiving and re-distributing block chunks to miners and exists in the form of a primitive web server, handling only HTTP GET and POST requests. This design was chosen as it will facilitate the use of the internet to communicate between miners on different networks, whilst demonstrating through a distinct lack of server-side processing of data, the ability of the miners to communicate directly with one another in a truly peer-to-peer manner. The only primitive processing executed by the server is that of adhering to a chunk blacklist specified by miners when requesting chunks. This is important so that miners can blacklist themselves and not get their own chunks back. It also demonstrates the ability of miners to chose which branches they want to accept chunks from.

#### Branch Reconstruction

Currently a branch reconstruction program demonstrates the process that would be followed by a patient or group of patients if they were to lose access to any given branch. The program queries data in the blockchain files in the relevant directories for foreign chunks from a given branch. The program then reconstructs the primary data of each block using the chunks by following the Reed Solomon Erasure Coding reconstruction algorithm.

#### Data

Currently the data is an arbitrary ASCII string. With further development, the data will be stored as standardised data records that will conform to a given schema. A schema used in a production implementation of the system would require extensive collaboration with medical professionals in order to produce a schema that accommodates enough variance of data whilst not impeding on medical research through poorly formatted datasets.

### Results

Below is the log of a minimalistic simulation with 3 miners generating two blocks each (not including the uniform genesis block).

```
Miner 1: Initialised and genesis block added to chain
Miner 2: Initialised and genesis block added to chain
Miner 0: Initialised and genesis block added to chain
Miner 1: Published chunks for block 1
Miner 2: Published chunks for block 1
Miner 0: Published chunks for block 1
Miner 1: Downloaded foreign chunks for block 1
Miner 1: Added block 1 to chain
Miner 2: Downloaded foreign chunks for block 1
Miner 2: Added block 1 to chain
Miner 0: Downloaded foreign chunks for block 1
Miner 0: Added block 1 to chain
Miner 1: Published chunks for block 2
Miner 2: Published chunks for block 2
Miner 0: Published chunks for block 2
Miner 1: Downloaded foreign chunks for block 2
Miner 1: Added block 2 to chain
Miner 2: Downloaded foreign chunks for block 2
Miner 2: Added block 2 to chain
Miner 0: Downloaded foreign chunks for block 2
Miner 0: Added block 2 to chain
```

First each miner generates a genesis block that has some standard data as well as the branch owners public key. The miners then begin generating some primary data for their first block. This data is a randomly generated 64 character string. The block head and primary data is then used to generate 5 chunks. These chunks are then published to the exchange and downloaded by other miners. The miners add these (now foreign) chunks to their blockchains and execute the same process to generate another block.

Below is an example of a blockchain with only a genesis block and one standard block. The standard block contains one foreign chunk.

```json
[
    {
        "body": "This is the first block in the blockchain",
        "head": {
            "chain_id": "558ffe69053c54722bb9933f87b8ec39aa7204b8ab4e3fd819153240..",
            "id": 0
        }
    },
    {
        "body": "5bipl5pqB4idTKaiBHUs65AQrTBaMlFevxiB9dD6MZPSTvhj2frTp93ahP7AJ",
        "foreign_chunks": [
            {
                "data": "36fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61ca..",
                "hash": "a8f852c979447f3f7b3fe4c2b6d8c8f0e1a13bbc135efb2cbbb5052d..",
                "head": {
                    "block_id": 2,
                    "chain_id": "ff91c1311116c1469e789a33cf1466e61f682c4ff7f693bf..",
                    "chunk_id": 3
                },
                "signature": 1168767186736185247057188947692667929143094761666159608..
            }
        ],
        "head": {
            "chain_id": "558ffe69053c54722bb9933f87b8ec39aa7204b8ab4e3fd819153240b..",
            "id": 1,
            "prev_block_hash": "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c.."
        }
    }
]
```

The only data in each block that is not reconstructed is the foreign chunks. This is one of the limitations of the system design.

### Progress Against Plan

At the time of writing, the project is currently slightly ahead of schedule. The original plan dictated a working implementation be finished by the 24$^{th}$ of February. Whilst this has already been achieved, the implementation could be further developed past the minimally satisfactory point. The project currently demonstrates a strong proof of concept but falls short of demonstrating proof of implementation. Development of the implementation is expected to continue in parallel with writing the dissertation. 

### Further Developments

The project still has a number of required features and desirable features which still need to be implemented in order to successfully demonstrate that the system is implementable.

#### Distributed Simulation

Developing the system to work entirely over existing protocols on the internet is essential in order to achieve the objective of the project. The exchange must be able to be reachable over the internet from any standard network. If the timeline permits, I would like to move the network to be purely peer to peer, such that the exchange is used only for peer discovery between nodes.

With further development, each miner will also be capable of continuously listening for queries and returning data, both individual records and requested chunks existing on its branch.  The reconstruction script will then be able to query the miners for chunks on their blockchain via the exchange, as this will more accurately represent how this would be carried out on a productionised system.

#### File Storage

A productionised version of the solution would be required to store many different types of files. Therefore, it would be very beneficial to develop the ability of the system to store many different formats of data on a blockchain. The blockchains currently exists in the form of JSON files which only facilitate the storage of ASCII data. Implementing this functionality would require either a significant redesign, or implementing a much less efficient system for converting files into ASCII data.

#### Security Features

A vital role of each miner is checking the validity of each block and chunk of data and this has yet to be implemented. In its current state, the miners make no attempt to check the digital signatures, or size of foreign chunks that they accept into their blocks. This leaves the network vulnerable to denial of service attacks and risks reducing the credibility of the network.

The initial design behind the algorithm dictated that with each foreign chunk accepted onto a branch, the miner would validate the block and hence the entire blockchain that the chunk originally pertains to. Further investigation is required into the feasibility of this design. Perhaps the miner need only validate the block in question and some number of previous blocks.

#### Miners scanning network

> TODO: Miners scan network to check that branches that they have chunks stored on are still operational

## Testing

### Unit Testing

Unit testing is the most reliable testing method, however the extent to which it can be implemented to the Medilanac program is limited. This is because many modules of the software rely on fetching and receiving data from a server (simulating a different miner). Therefore the process of designing and building a test harness that simulates a miner for the test module to interact with is not feasible within the time constraints of the project.

However, many modules can be tested using unit testing with relative ease. Modules for cryptography, blockchain validation and merkle tree encoding are all used by multiple other modules across the system. They are all coded to be functional modules and can therefore be tested with input/output combinations.

The merkle module tests consist of tests for both all combinations of input types. The module is tested for lists of type `int`, `string` and `bytes` for lists of even and odd length. The network protocol does not require there to be a standard oder for files, that is, medical data can be uploaded to the blockchain in any order the miner chooses. This was a deliberate design choice. As there is no necessity for data to be in any specific order for the network to function. Adding unrequired complexities to the schema of the protocol increases the complexity of the scheme and therefore the barrier to entry for miners and therefore users.

All cryptographic algorithms used for this project were implemented using the pyCrypto library. This library is open source and undergoes sufficient testing outside of this project and is therefore not tested as part of this project. However, the crypto module that serves as an extra layer of abstraction for the pyCrypto module that has been written as part of this module requires testing. Some methods of the crypto module are tested using standard input/output comparisons, such as for checking that the output of the hash function has does not change during development. Metamorphic testing has also been implemented, testing the following metamorphic relations:

- The hash of two different strings should not be equal
- The message output from sequential encryption followed by decryption of a message should be equal
- The cipher texts of a message should not be equal when encrypted with two different keys
- The cipher texts of two different messages should not be equal when encrypted with the same key

The blockchain validation module can also be unit tested as the validation module, similarly to the cryptographic module, must be able to be replicated on multiple machines across the network. Therefore the validation algorithm can be tested by passing in a series of valid and invalid blockchains. The mechanism (oracle) for determining wheather the program has passed or failed, that is, the validity of each blockchain used as a test case is fundamentally the software itself, under the supervision of the developer. That is, the valid blockchains were generated using a version of the software that was judged to be correct, these valid blockchains were then either directly used as valid test cases, or altered in some way as to make them invalid and used as invalid test cases for all subsequent versions. Whilst using the output of a previous version of the software as an oracle for the later versions is not an ideal approach as it risks carrying unknown bugs/errors through, it is the most feasible option and is still capable of flagging an unintended change to the output of the software.

### E2E

Another way to test the software is by running an end-to-end test. The test script runs the software from start to finish with preconfigured parameters. Each branch is then attempted to be reconstructed. If any branch fails then the output of the test is also a fail. If there are any errors during the simulation, these will also trigger a failed test.

A caveat with this method of testing s that the test script ignores the final two blocks on each blockchain. This is to account for the complications and errors resulting from the termination of the software. Considder thhe following high level logical flow stages of the miner process (incomplete as some stages have been omitted):

1. Generate/gather primary data of block
2. Retrieve foreign chunks
3. Update block merkle tree
4. Generate chunks of block
5. Submit chunks to server for distribution

Note that it is not possible for each miner to generate chunks for each new block until after it has retrieved the required number of foreign chunks from other miners. This is because the merkle tree of these chunks is included in the block data, therefore the hashes of each chunk must be known before a block can be completely generated. As each miner in the system is running in parallel for a finite amount of time/iterations, there fundamentally must be a first and last miner to terminate. The final miner to terminate then, will be attempting to distribute, and potentially also gather chunks to/from a network with no other active miners. The miner will therefore not be able to submit his chunks to the network and a full branch reconstruction may not be able to be achieved.

This is not a problem of the protocol as a productionised version of the software would never need to handle a complete termination of the network. *If it  did, there would be no purpose to distributing or retrieving chunks anyway.*The network need only handle single miners leaving/joining at any time, which it indeed does. Therefore, to handle this eventuality, the end-to-end test script checks that each block of each blockchain can be reconstructed with the exception of the final two blocks.

### Reconstruction fault tolerance

> TODO: find the amount of branches that can be removed before a branch cannot be reconstructed
>
> - Run various tests and graph

In order to investigate how the fault tolerance of the network is related to the data redundancy introduced using erasure coding, several simulations were undertaken with data collected about each one. The simulation involved multiple complete runs of the software, each with 50 miners generating six blocks on the blockchain. However, with each subsequent simulation, the ratio of the k to m was changed in order to vary the amount of data redundancy.

As the network is more susceptible to being affected by the quantity and timing of interactions between miners, rather than the amount of data behind each interaction, the value of m remained at a constant value of 10 any only the value of k was altered.

With each simulation, 20 miners were then chosen at random to be tested out of the 50 miners participating in the network. The test involved the sequential removal of branches from the network, testing to see if the branch belonging to the miner under test can be successfully reconstructed from the rest of the branches still present. This is continued until the branch can no longer be reconstructed. The number of branches that have been removed is then recorded and the next miner is chosen to be tested, with all previously removed branches returned to the network. The reconstruction of the branch need only to successfully reconstruct the first 4 blocks on the blockchain in order to pass the test. This is to account for any chunks that are missing on the network resulting from the termination of the simulation, as outlined in **TODO**.

![ft_results](Diss.assets/ft_results.png)

We can trivially see from the results that the network fault tolerance increases linearly with data redundancy. This is to be expected as with a higher degree of data redundancy, fewer chunks must be sourced to reconstruct each block. We can also see however, that the relationship is not symmetrical. This is resulting from the criteria required for a reconstruction to be classed as successful. We defined a successful branch reconstruction as being able to reconstruct all block on the branch excluding the final two which are not considered. Therefore, the probabilities of each individual block being successfully reconstructed must be multiplied in order to obtain an estimate for the probability of the branch being successfully reconstructed. We can therefore introduce and effective increase in fault tolerance by designing each blockchain such that they store hash links to multiple previous blocks, instead of just one, as outlined in **TODO**.

>  TODO: Check "symmetric" for relationship

The benefit of an implementing a high data redundancy rate is clear, each miner/user can cope with a higher number of nodes failing before losing the ability to recover data. However this directly affects the amount of data that each node is required to *donate* to the network. If the data redundancy rate is too high, the network will become inefficient and the barrier of entry will increase costs to miners/users.

### Malicious Miner

> TODO

### Bugs

> TODO
>
> - last blocks in blockchain chunks don't always get submitted - termination of network tricky
> - Thread lock with recursion
> - Foreign chunks being left in and submitted- storage explosion

---

#### Miner

The miner can be tested to check that the blockchain it produces is valid to the extent that all hashes and signatures are correct. The chunks posted to the exchange can be tested to ensure that the chunks can be successfully reconstructed into a valid block using all different permutations of the chunks, and that the reconstructed data is identical to the primary data of the block it was generated from. Tests checking that the miner only accepts records that have been correctly signed should also be implemented.

#### Exchange

The exchange is possibly the simplest module of the system to test as each test-case can simply submit a sequence of chunks and with various signatures and branch ID's, and then request chunks back. The returned chunks can then be checked for validity by checking that the branch ids are not blacklisted in the request, and by checking that the chunks are identical to those that were submitted.

#### Network

Testing of the network as a whole can be achieved by introducing malicious nodes attempting to cause the either the loss of data, flood the network with malicious data, or introduce data without hosting their required amount. The network can also be tested by introducing a number of nodes that encounter a fault and become unusable. This should give a good indication of the fault tolerance of the network.

#### Metamorphic Holistic Testing

Testing of the individual modular components of this project will not suffice to ascertain security of the network. While it is necessary to implement a test suite for the miner module, exchange, and reconstruction software individually, we must also scrutinise the network as a whole in order to establish how it fares against malicious intent and inevitable faults. 

Metamorphic testing is a way of testing software in which tests do not compare a set of inputs against an expected output, but rather analyse relationships between multiple input-output pairs [15]. The following metamorphic relationships are expected to hold true and can therefore be tested:

- Average bytes stored per branch should remain constant when varying the number of branches/miners on the network.
- The fault tolerance should be mathematically related in some (currently unknown) way to the recovery ratio of the erasure coding code rate.
- The resulting blocks created by any combination of chunks originating from the same block should all be equal.
- Foreign chunks accepted onto on branch should not be rejected from another.

> TODO:
>
> Miners can flood the network with chunks, storing a chunk on the network multiple times

## Reflection

> TODO

- Intro
  - I am pleased with the quality of code
  - Good software engineering practices used
    - Testing
    - Agile
    - Source control - single handedly saved the project during the sudden relocation
  - Plan changed as a result of the sudden relocation
    - Primary dissertation supervisor and module set up changed
- Format the blockchain is a different way other than ascii
  - not ideal as all ascii needs to be parsed
  - State what format I would use
- Whilst developing the program under agile methodologies, i would think about/put more emphasis on thinking about higher level problems and attacks throughout the problem, rather than lower level attacks as these can be considered later on in development
- What have i learnt?

---

Overall I am pleased with the outcome of the project. Throughout the project I utilised numerous software engineering best practices, including source control, test driven development, and the agile methodology. The program has been written to produce extensive logs that can be effectively utilised for debugging as well as clarifying the logical flow of the program. Resultantly, the code produced is of a high quality.

I utilised a variation of the agile methodology to produce the code and dissertation for this project. The variation dictated that each sprint last a day of work, with the intended increment to the minimum viable product being defined at the start of each iteration. This aided the development of the project as it reiterated the idea that the direction and design of the system was dynamic and continuously changing. However, in future projects such as this, I will put more emphasis on high level design considderations throughout. I found with this project that it was all to easy to get distracted and focus too intently on the miner design details and security vulnerabilities, sometimes to the detriment of broader ones. For example, It was not until the later stages of testing the project that I discovered the defect outlined in section **XXX**. Had i placed more consideration into an overview of the system, I would have perhaps spotted this shortcoming earlier and had the opportunity to design measures to rectify it.

> TODO: Write section on miners spamming the same chunks to the network multiple times

Test driven development (TDD) is... TDD was used for the areas of the project that it could be feasibly applied to without adding excessive workload. TDD helped to ensure that the minimum viable product criteria was not exceeded for the modules it was applied to, as well as assisting in the design and specification of the API for each module.

Approximately half way through, the project had to abruptly be relocated to a different university. The decision to use source control that was sufficiently backed up in multiple locations saved the project from what would most likely have been weeks of delays and setbacks. Git also helped develop features and improvements that could easily be abandoned at a later stage, something that it crucial when working to the agile methodology.

The relocation did however alter the deadline and marking criteria of the project. Resultantly the project plan had to be adapted to meet the new deadline and requirements. Throughout the later stages of the project, I adhered to the project plan with discipline. However, whilst remaining on schedule, I did not embrace the opportunity to get ahead of schedule as much as I otherwise could. Although I believe it to be impossible to foresee the factors that affected the timeline of the project, in the future I would put more emphasis on remaining ahead of schedule in order to maximise the slack time available for unforeseen setbacks.

In order to design a system that is build on top of blockchain, it is imperative to have a good understanding of the technology to include it's strengths, weaknesses, and vulnerabilities. Therefore a significant proportion of this project was allocated to expanding my prior knowledge in this field, and conducting extensive research into the wider and narrower domain related to subject of the project.

### Implementation

#### Blockchain Data Format

If I were to complete the project again I would choose to design the system such that it stores the blockchain in a format other than ascii data. The reason being that it is generally not good practice to store files as ascii data as it is a relatively inefficient method of storage. Although sufficing for this project, complication arise when large files are required to be stored on the blockchain. As the data is stored in JSON format, the entire blockchain must be parsed in order to load the data. As previously mentioned, this can be mitigated by splitting each block up into its own JSON file, however this is still not a complete solution in an implementation where blocks are gigabytes or even terabytes big. Instead I would implement a design such that each block was a zip archive such that each file could remain in its original form, storing only the block headers as ascii data. The merkle tree in the block headers would then link to either the files themselves, or even a uniform size of fragment of each file in order to speed up the miner validation process that is carried out with each exchanging of chunks.

#### Technical Development

The decision to use Python and various individual libraries for the development was overall successful. I believe that the learning cure was more gradual than it would be had I taken other, more framework heavy, routes such as using NS3. This route also enables the cure to be varied over a broader range of technologies to include multiprocessing, web servers, encryption, erasure coding. I believe the experience gained with this array of more general technologies will be more beneficial than more in-depth experience with a single, less widely used framework.

## Conclusion

To date, I have implemented a working simulation of miners adding data to a blockchain and sharing chunks of each of their blocks on their chain with one-another. I have written software capable of reconstructing the primary data on any one branch from secondary data on other branches. The system currently has very few of the necessary security features implemented. In it's current state, malicious actors could easily take down the network by flooding it with null data as they would not have to prove storage of an equal amount of secondary data.

Traditional blockchain technology can cope with nodes leaving and rejoining the network exceptionally well. This is because the complete blockchain is stored on all nodes [2]. Therefore, nodes can simply query another node upon rejoining. However, the system laid out above was designed so that this is not the case. Therefore it currently has very little tolerance for nodes wishing to leave, as data they were previously hosting must be reconstructed and new primary storage must be set up. The system currently has no functionality for patients (or simulations thereof) to add data to a branch of the network. The necessary privacy and security features will also be required. The simulation is also not currently able to communicate over the internet or store non-ASCII data.

Research and system design of how a proof of storage protocol could be implemented and added to the system has yet to be carried out. This is fairly crucial to the network as it prevents the ability of *free-riders*, that is, parties to the network hoping utilise the storage offered by other nodes, whilst not storing an adequate amount of others data themselves.

## Works Cited

1. Daniel Kahneman. Thinking Fast And Slow. Farrar, Straus and Giroux, 2011. 
2. Satoshi Nakamoto. Bitcoin: A peer-to-peer electronic cash system. 2008. 
3. Marc Pilkington. Can blockchain improve healthcare management? 
4. The Economist. Rise of the machines. 2015. 
5. Mandl KD Weitzman ER, Kaci L. Sharing medical data for health research: The early personal health record experience. 2010. 
6. Blockchain. "Size of The Bitcoin Blockchain from 2010 to 2019, by Quarter (in Megabytes)." *Statista*, Statista Inc., 30 Sep 2019, https://www.statista.com/statistics/647523/worldwide-bitcoin-blockchain-size/
7. https://www.bitcoinmarketjournal.com/how-many-people-use-bitcoin/
8. Azaria, Asaph, et al. "Medrec: Using blockchain for medical data access and permission management." *2016 2nd International Conference on Open and Big Data (OBD)*. IEEE, 2016.
9. K. D. Mandl *et al.*, “Public standards and patients’ control: how to keep electronic medical records accessible but private,” *BMJ*, vol. 322, no. 7281, pp. 283–287, 2001.
10. Liang, Xueping, et al. "Integrating blockchain for data sharing and collaboration in mobile healthcare applications." *2017 IEEE 28th Annual International Symposium on Personal, Indoor, and Mobile Radio Communications (PIMRC)*. IEEE, 2017.
11. Xia, Q. I., et al. "MeDShare: Trust-less medical data sharing among cloud service providers via blockchain." *IEEE Access* 5 (2017): 14757-14767.
12. Fan, Kai, et al. "Medblock: Efficient and secure medical data sharing via blockchain." *Journal of medical systems* 42.8 (2018)
13. Zyskind, Guy, and Oz Nathan. "Decentralizing privacy: Using blockchain to protect personal data." *2015 IEEE Security and Privacy Workshops*. IEEE, 2015.
14. Weatherspoon, Hakim, and John D. Kubiatowicz. "Erasure coding vs. replication: A quantitative comparison." *International Workshop on Peer-to-Peer Systems*. Springer, Berlin, Heidelberg, 2002.
15. Segura, Sergio, et al. "Metamorphic testing: Testing the untestable." *IEEE Software* (2018).
16. Cong, Lin William, and Zhiguo He. "Blockchain disruption and smart contracts." *The Review of Financial Studies* 32.5 (2019).
17. Perard, Doriane, et al. "Erasure code-based low storage blockchain node." *2018 IEEE International Conference on Internet of Things (iThings) and IEEE Green Computing and Communications (GreenCom) and IEEE Cyber, Physical and Social Computing (CPSCom) and IEEE Smart Data (SmartData)*. IEEE, 2018.
18. Katina Kralevska, Applied Erasure Coding in Networks and Distributed Storage
19. Nathan Heller. "Estonia, the Digital Republic"
20. Mahdi Zamani. "RapidChain: Scaling Blockchain via Full Sharding"
21. Wood, G.: Ethereum: A secure decentralised generalised transaction ledger. Tech. Rep. EIP-150, Ethereum Project – Yellow Paper (April 2014)
22.  Underwood, S.: Blockchain beyond Bitcoin. Communications of the ACM 59(2016).
23. https://www.bbc.com/news/technology-48853230
24. https://www.cbeci.org/
25. https://www.bbc.com/news/technology-44682369
26. Luc Wood, interview
