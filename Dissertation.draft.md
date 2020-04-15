# Dissertation

## Abstract

Medical data of an individual is commonly stored in a fragmented manner in many different locations which restricts ease of retrieval by patients and the collation of large useful datasets by researchers. Furthermore, studies have shown that patients benefit from a clear holistic view of their medical data [9]. Blockchain has the potential to free up medical data, advancing research and improving the healthcare delivery. At the same time blockchain technology enhances patient privacy and security. My design, Medilanac is a blockchain networking design which, unlike other similar implementations, stores medical data on the blockchain itself. Medilanac proposes a new protocol to overcome the inherent inefficiencies of storing large datasets on the blockchain posed by the technology itself. Therefore maintaining the data validation and recovery functionality of standard blockchain technology, and at the same time allowing for the storage of large and diverse data sets.

## Background and Motivation

The increase in data harvesting and storage in recent years has led to an increase in the widespread development of artificial intelligence systems for statistical analysis and pattern recognition on large datasets for the purpose of improving healthcare. Consequentially, conversations about the trade off between advancements in medical research and the right to privacy of the individual have become mainstream [3]. 

For many medical professionals, their skills development and consequently their contributions to healthcare are inhibited by a lack of accurate and timely feedback [1]. AI systems do not suffer from such a problem. With large datasets, AI systems facilitate data analysis that can divulge complex patterns linking specific practices/decisions undertaken during treatment of individuals, with significant outcomes and degrees of success that would otherwise not be elucidated. Newly discovered practices can then be adopted, improving healthcare [4]. They are able to examine, in detail, orders of magnitude more medical records than human doctors can in their finite careers, learning and improving from each one, allowing them to give more accurate diagnoses and recommendations for treatment. 

A decentralized, international medical database which is available to all could facilitate significant improvements in medical practices. The ability to compare the short-term and long-term outcomes of treatments performed in different locations around the world, would facilitate analysis of the strengths and weaknesses of diverse practices, and serve as a major catalyst for improvement [5]. Providing a clearer view of their complete medical records would also offer patients more immediate benefits [9].

## Literature Review

Many attempts have been made to combine medical data and blockchain technology. However, none has managed to find a solution to the inherent problem with blockchain which is that it is poorly suited to storing large amounts of data [2]. This is because every user (node) on the network must have a complete copy of the entire blockchain.

As the blockchian is an *append only* data structure, if we were to merely create a protocol that allowed for medical data to be stored on a standard blockchain, it is likely that it would either quickly grow to an unmanageable size or would not be able to store adequate amounts of data in a timely manner; From Q3 2018 to Q3 2019, Bitcoin, the most prominent cryptocurrency built on top of a blockchain, saw its blockchain size increase by 57.764 GB to a total of 242 GB from an estimated 5.8 million active users [6,7]. We can therefore calculate that the average annual blockchain data contribution is approximately 10 KB per person per year. Consequently, if someone wants to store and retrieve the annual transaction data of say 5000 people, amounting to 50 MB, they must store the entire 242GB blockchain, some 4840 times more data than that of which they desire. When considering a typical small GP clinic hoping to store the medical records of its 5000 registered patients on a system equivalent in design to bitcoin but repurposed for the storage of medical data, the problem is clear [26].

### Blockchain

Blockchain was originally conceptualised by an individual acting under the alias of 'Satoshi Nakamoto' for the purpose of creating a decentralised trust-less peer-to-peer cash system [2]. Their paper proposes a public ledger that is append-only and completely immutable. That is, once something has been added to the ledger and accepted by the majority of the rest of the network, it is nearly impossible to change it. To do so would require cooperation of at least 51% of the computing power on the network, something that the protocol relies on being unachievable for the security of the network.

The protocol hosts an ongoing open competition pitting contestants (*miners*) against each other, all attempting to be the first to solve a computationally laborious maths puzzle. The winner is able to publish the next block (containing users data) on to the blockchain and receive their reward for doing so. The maths puzzle is such that it is difficult to find the answer, but easy to verify the correct one. Therefore once any given miner successfully finds the answer to the next block, all other nodes can quickly verify it and begin working on finding the solution to the subsequent block.

![](Diss.assets/Blockchain_nb.png)

The majority of the data within each block is data submitted by the end users to the miners for publishing. This data must also meet a set of criteria that all of the miners agree to. If the data does not meet the accepted criteria, it will be invalid and will not be accepted onto the blockchain by the rest of the network.

#### Smart Contracts

In recent years, the most significant developments have emerged in the form of smart contracts. Blockchains such as the Ethereum blockchain allow for code written in Turing-complete languages to be added and executed on the blockchain [16]. The advent of smart contracts has meant that functionality of blockchains has moved beyond just the mere storage of data, and towards the advent of distributed computing [21, 22]. It is now possible to execute complex and immutable programs in predefined, predictable ways. Untrusting parties are therefore able to cooperate in ever increasing amounts, whilst maintaining assurance against security breaches.

#### Blockchain Sharding

Zamani et al introduced a method of sharding a blockchain such that minimal node inter-shard validation is required [20]. Validation is carried out by a *committee* of nodes elected for each *epoch*. The committee of each shard is responsible for communicating with the committee of other shards in order to validate data on their own shard for which the process of validation requires data on a different shard. Minimal validation is undertaken by the majority of nodes on the network, and very few of them are required to process data from other shards with each *epoch*.

### Erasure Coding

Data redundancy is an inevitability when ensuring reliability in a network [18]. Erasure coding is a way of maximising the reliability whilst minimising the data redundancy required to achieve it. The encoding algorithm is a method of protecting data $d_{o}$ from corruption/loss by splitting the data into $k$ *fragments* ($ f_{i}, i = 1..k$) and then encoding those fragments into $m$ *chunks*, $c_{i}, i = 0..m-1$ such that the original data can be recovered with any number $n, n \geq k$ of the chunks [14]. Each of the encoded chunks is one of the linear combinations of the fragments of $d_{o}$. The summation of size of all encoded fragments is greater than the size of the original data, $ \sum_{i=0}^{m-1}size(c_{i}) > size(d_{o})$; hence the aforementioned inevitable redundancy.

Erasure coding allows data that has been fragmented across different physical locations to be recovered in the event of the loss of *some* of the data, whilst simultaneously minimising the amount of data redundancy required. As such erasure coding has seen ample use within systems that need to be able to tolerate failures such as disk arrays, archival storage, data grids, or distributed storage. With the absence of erasure coding, systems such as these would have to resort to storing complete backups of the entire data, or risk data corruption if even a single part fails.

#### Blockchain and Erasure Coding

Blockchain and erasure coding have the ability, when used in conjunction, to solve many problems requiring a high degree of fault tolerance in a trust-less environment. The former enables bit-level validation end security, whilst the latter provides the ability to recover data in the event of a partial loss.

Perard et al propose the idea of a Low Storage Node on a blockchain [17]. Their system design incorporates erasure coding such that nodes need not store a copy of each entire block, but merely a single chunk of data from each. Greatly reducing the amount of data each node is required to store. Their system is designed to be more accommodating to nodes with less storage capacity but is not equipped to deal with a the heavy data requirements of medical data on a large scale. Furthermore, the network requires miners to compete to add blocks to the network. This is a hugely inefficient design as it requires significant infrastructure and electricity to maintain. A study from The University of Cambridge found that Bitcoin's annual energy consumption is roughly in line with that of Switzerland [23, 24]. These are costs that are ultimately passed onto the patients.

> Explain more why it is not equipped

Furthermore, their solution In forcing all nodes to store the same (reduced) amount of data and is therefore not suitable for the storage of medical data as it fails to handle the inevitability of some nodes producing more data than others. With no motivation to moderately add data to the network, a 'tragedy of the commons' situation emerges such that the size of the blockchain would rapidly explode and become unusable.

### Blockchain In Medical Data

#### MedRec

One of the most notable current implementations combining blockchain and the storage of medical data is that of MedRec, a Medical record storage system built to work on top of the Ethereum blockchain [8]. The system uses smart contracts to manage the permissions of medical record viewership, incentivising miners with the reward of anonymised medical data that can be used for research. The medical data itself is stored on healthcare providers databases who allow anyone who has the permission of the owner (according to the blockchain) to view or update the medical records.

MedRec gives users a comprehensive and holistic view of when and by whom their medical data has been changed, which benefits patients [9]. Privacy concerns are combatted with transparency by allowing patients to more easily see what information can be derived from their complete set of medical data. Patients can therefore be more confident that their data is unlikely to exist anywhere else such that it could be aggregated, allowing for more information to be derived without their knowledge.

The greatest weakness of this approach is that the individuals must still trust their service providers to offer a *good* service. Individuals must trust that the provider will sufficiently backup and manage their databases, so that their data will not be lost. If the data itself is lost then the provider would not be capable of retrieving it for the patient and the smart contract on the blockchain would become void. Patients are required to trust that the provider will implement adequate security measures to their databases in order to prevent their medical data being stolen and their privacy breached. Similarly, they must also trust that the provider will not sell or share their data without the permission of the patient, no guarantee of which is given by the permissions of the blockchain. Finally the patient is required to trust that the provider will not withhold the data from the patient or any authorised party. It is easy to assume that the business model of the provider would incorporate some assurances in relation to these issues, however business decisions are often overruled by governments or other subjective motivations.

#### e-Estonia

Many similar system designs have been proposed by others, all of which require data to be stored off-chain, and only access rights to be stored on-chain [10, 11]. One such system is that of the KSI blockchain system used for the Estonian "e-Estonia" initiative [19]. The national blockchain system stores data and backups on servers in a conventional manner. The blockchain is then combined with a time-stamping server to ensure authenticity and time of permissions. This system is therefore predominantly centralised; the government has complete control over the time-stamping server, databases and blockchain itself. It is theoretically possible, therefore, for the government to edit and remove data on the blockchain, or forge a timestamp for data. This approach is therefore not capable of storing data in a decentralised manner.

#### MedBlock

The system proposed by Fan et al proposes a distributed ledger containing only summaries or electronic medical records (EMRs), the detailed sources of which remain in the databases of health service providers [12]. The EMR summaries also contain the cryptographic hashes of the source data to ensure they are tamper-proof. However, patients must still trust the service providers to competently and ethically store the full EMRs for them, which they often do not [25], and therefore many of the same issues arise as with the MedRec system.

#### Third Party Hosting

Zyskind et al put forward a system where a data storage service is trusted with an encrypted version of the medical data, and a blockchain used for logging and permissions control [13]. The idea of encrypting data stored by the service provider offers good protection against unauthorised sharing of the data as it is of no use without the key. Therefore a system design ensuring that the party storing the patients data never possesses the key to said data eliminates this requirement of the patient to trust in the provider to not share their data without permission. However, there is no guarantee that the data storage service will not withhold or lose the (encrypted) data. Therefore the patients must still trust the provider to store their data competently and act within the confines of their agreement.

## Methodology

This project is tasked to build a proof of concept of a system for which implementations could be derived from that aim to address the task of creating an international decentralised medical database. The goal of this project is therefore to produce a simulation that serves as a proof of concept only, with considerations of technologies that would likely be used, as well as barriers that could hinder such a system from existing.

This project incorporates multiple different stakeholders. As such, higher level functional requirements can be defined that apply to the system design as a whole, while lower level non-functional requirements apply only to their respective stakeholders.

### Functional Requirements

The system must satisfy all of the following requirements:

1. Data must be stored such that the data owner does not need to trust the data storer to: 
  1. Adequately protect data from loss and theft,
  3. Not share data without permission from the data owner,
  4. Not withhold data from owner.
  
2. Data must be able to be retrieved in a timely manner.

3. The data owner must be able to remain in control of their data in that:

   - They have the ability to read and write to their data

   - They have the ability to control which individuals/parties have the ability to read and/or write to their data

4. The user must not be required to store an *unreasonable* amount of extra data when adding their own.

### Non-functional requirements

#### Data Storage Provider (Miner)

The network protocol must ensure that all blocks added to the network conform to the following set of standards, and that blocks failing to do so are not accepted by the rest of the network:

- Each block must conform to a predefined set of standards that describe the structure and size limits of a data.
- Each block must be signed to ensure authenticity.

- Each block must contain a number of foreign chunks such that the size of data used by the foreign chunks is equal to the size of data used by the branch's own data, plus the threshold amount.
- Blocks must be split up into chunks using erasure coding and submitted for storage on other branches.
- Each chunk must be signed to ensure authenticity.

#### Patients (Users)

- Users/patients must add data in a format the conforms to a specific schema.
- Data must be signed.
- Private data must be encrypted.

### Plan

The plan for this project is to start by researching previous works relating to the use of blockchain for the storage of large data sets including medical data, before designing an algorithm and building an implementation.

A.  Project proposal

B.   Research previous works

C.   Design an algorithm

D.  Write interim report

E.   Build an implementation

F.   Write dissertation

![Gantt](Diss.assets/Gantt.png)

## System Design

### Overview

The system design dictates that user data is stored by secondary parties referred to from here on as miners. Each user-chosen miner will be the primary storer of said users data. This allows for the inevitability of user incompetence as the miners can be the ones who build user-friendly interfaces and offer support to users. This increases the accessibility to the network for users, a crucial consideration when designing blockchain systems in order to not hinder their widespread adoption [27].

The miners will store user data in the form of a blockchain. The blockchain ensures that data, once added, cannot be altered by any party, without invalidating said data. Instead of a single blockchain with many miners competing against each other, the proposed system requires each miner to have their own permissive blockchain shard (branch), that is, a blockchain that can only be added to by the miner that it was created by. The use of digital signatures can verify the author of a block. Furthermore, miners can do this without being required to solve any maths puzzle (proof of work). This means that every miner (node) on the network has complete control over when they add extra blocks to their branch. As the miners are the only ones storing a full copy of their blockchain, they are also required to share their entire chain with anyone who wishes to query it. This is necessary for the miner to pass the validation process of other miners, without which, they will not be able to store any data on the network. 

After sourcing all of the desired data to be stored on a single block, the miner will generate a merkle tree for all the files on the block and store this as part of the block header. The miner will then encode the block using an erasure coding algorithm into multiple smaller fragments referred to from here on as 'chunks'. Chunks are the erasure code fragments of blocks on the network that can be reconstructed (with any number $n \geq k$) into the original block. Therefore, any party wishing to reconstruct any given block, need only require $k$ chunks. 

These chunks are then distributed out to other miners on the network. Similarly, chunks from other miners are retrieved and the validity of both the chunk and the miners is verified using a process that will be outlined i section **XXX**. These chunks pertaining to data on the blockchain of miners other than the subject, from here on referred to as 'foreign chunks', is added to the miners block being generated. In this way, data redundancy is achieved and distributed across the network, allowing for safer storage of data.



![Adding a block C4 to branch C requires the miner to add chunks from blocks in other branches to C4](Diss.assets/Adding_Block.png)

*Adding a block C4 to branch C requires the miner to also add chunks from blocks in other branches to C4.*

Resultantly, data can then be reconstructed in the event of a loss of a branch, from chunks that are stored on other miners branches on the network. This can be achieved by querying other miners for chunks pertaining to a given branch, and retrieving those chunks. The chunks can then be used to generate the original block data using the inverse of the previous erasure coding algorithm. This capability therefore accounts for the eventuality of a malicious or incompetent miner, by allowing users to reconstruct their data from other nodes on the network.

#### Miner Peer Discovery

Communication between miners is peer-to-peer (serverless), this is crucial in order for the network to remain decentralised. Therefore, the network must implement a mechanism for peer discovery. Typical peer discovery algorithms consist of the node attempting to join the network querying one or more previously known nodes for the addresses of any others on the network that they are aware of. This is then repeated for any nodes they find until a sufficient number have been discovered. 

For the simulation, I have chosen to add an exchange to the design of the system that will act as the pre-known node. However the exchange will not act as a miner and will serve the soul purpose of facilitating peer discovery. Additionally, the miners will receive a complete list of all nodes on the network from the exchange and will therefore not need to query known miners for the addresses of other miners. This design was chosen because it is the simplest mechanism for peer discovery that will facilitate the serverless exchange of data between nodes on the network.

The decentralised nature of the network is not affected by this design as the exchange has very little control over the network as it is only able to listen for miners announcing their presence, and return a list of all miners in existence, along with their url, upon request. No significant data processing or validation is undertaken by the exchange, the miners must decide which other miners to trust through the process of miner validation. Additionally, if this design were to be implemented in a production environment, multiple exchanges could exist all in competition with one another, further reducing the threat of centralisation.

#### Block Erasure Coding

One of the design challenges with splitting each block up into pieces and storing them in different locations is that blockchain protocols require every single byte of a block to be present. If a single one is missing, the hash, and therefore the block, cannot be verified and the blockchain is broken. This means that every subsequent block on the blockchain also cannot be verified. The only way to recover the data is by using a brute force search for the value of each bit until the combination that matches the block hash is found. Therefore if a single chunk was lost, the entire branch from that block onwards would become invalid and could not be feasibly reconstructed. For the system to be useable, it must have a reasonable fault tolerance. We must therefore incorporate a way to allow for some chunks to be lost and still be able to reconstruct an entire block.

With each block added to their blockchain, the miner must include a number of *chunks* of blocks from the blockchains of other miners. Chunks are the erasure code fragments of blocks on the network that can be reconstructed (with any number $n, n \geq k$) into the original block. Data on a branch pertaining to another will from here on be referred to as *secondary* data consisting of foreign chunks. The data created/added by the miner of a blockchain will be referred to as *primary data*. Hence primary data on one branch is encoded into chunks and becomes secondary data on a different branch. In accepting secondary data, miners are essentially contributing to the back up of other blocks on the network. The required ratio of primary/secondary data in each block on the network is defined by the protocol, but will have to be a minimum of $(m/k) S_{p}$ where $S_{p}$ is the size of the primary data in each block. 

After adding the block, the miner must use erasure coding to encode the block's primary data into chunks, and send to other miners on the network to store on their blockchains (as foreign data). If the miner loses access to a chunk on another branch, they must replace it on a different branch in the network in order to maintain a sufficient backup on the network.

![B](Diss.assets/Block.png)

*Logical overview of the contents of each block on a blockchain.*

> TODO: Remove 'confirmation signatures' from image

Without erasure coding, the miner of any given branch ($b_{i}$) storing a fragment of any block originating from another ($b_{j}$), would have the power to corrupt the backup of the corresponding block. This would therefore require that the nodes have a certain degree of trust between one another, serving as an inhibition to the network. Erasure coding is used so that in the event of patients losing access to a branch, albeit from loss of data or from an uncooperative service provider (miner), the primary data of a branch can be reconstructed with $k$ foreign chunks, as opposed to all $m$ fragments. Therefore, as long as a large enough proportion of the nodes storing the data ($k/m$) successfully return the data, we can reconstruct all primary data on a branch.

For the network to function correctly a certain proportion of nodes must be cooperating with the rest of the network. This proportion is hypothesised to increase linearly with the amount of additional erasure code that is generated for each block, and the number of branches on the network.

In distributing chunks obtained from encoding blocks using an erasure coding algorithm, the protocol introduces a certain amount of data redundancy. Therefore when attempting to reconstruct a block in the event of a miner failure, the party attempting to reconstruct the block need only obtain a fraction of all the chunks stored on the network to reconstruct the original data. Hence it is guaranteed that any individual block on a network with a data redundancy of 40% can be reconstructed with any number of chunks greater than that which equates to 60% of all chunks for said block on the network. However, as the blockchain is split up into blocks that must be individually reconstructed, the blockchain as a whole is not guaranteed to be able to be reconstructed with any number of chunks $n, n\geq k n_b$ where $n_b$ is the number of blocks. 

### Exchanging of Chunks

It is in each miners interest to have their primary data stored on a reputable blockchain, rather than an untrustworthy one. This is because the network as a whole has an average fault tolerance of nodes. This fault tolerance can be reduced for any miner storing chunks on a branch belonging to a miner that is not acting in accordance with the protocol of the network. Therefore each miner must perform some kind of verification procedure when distributing and retrieving chunks.

The structure of each block has been designed with this in mind. The header of each block contains two merkle trees, one for all primary data items, and one for all foreign chunks contained within the block. This allows any miner ($A$) attempting to validate the blockchain of another miner ($B$) to first query $B$ for a summary of their blockchain. This summary comes in the form of the block headers of some or all of the blocks on the blockchain. The block headers are only a fraction of the size of the entire block, enabling quick retrieval over finite bandwidth. $A$ can then challenge $B$ to return any specific files as chosen by A. These files can be verified to be in the blockchain using the merkle tree. In this way, it is very difficult for $B$ to appear to be storing data without being able to produce specific fragments of it on demand. After several  sections of data that were randomly chosen by $A$ have been produced by $B$, $A$ can be confident that $B$ is storing the data they claim to be. Therefore, any miner attempting to use the backup capability of the network without also contributing to it by storing and serving other miners data, will struggle to find any other miners on the network willing to store their chunks.

### Branch Reconstruction

Branch reconstruction can be carried out by any party at any time, however its utility is designed to allow data owners to retrieve their data in the event of a failure of a miner. Reconstruction is carried out by querying all/enough miners on the network for chunks pertaining to the specific branch that is being reconstructed. Once enough chunks for each block have been retrieved according to the redundancy threshold set out in the protocol ($k$), the block can be reconstructed using the inverse of the predefined erasure coding algorithm used to encode the block into chunks. So long as all previous blocks can also be successfully reconstructed, the block can be validated, although there are ways of mitigating this limitation that will be outlined later.

It is important to note that as only the primary data of each block is split into chunks and distributed across the network, only this data can be reconstructed. Foreign chunks of blocks cannot be reconstructed. This is because foreign chunks are backups of primary data on other branches. Requiring foreign chunks to be stored again would create a recursive storage requirement that would quickly render the network incapable of storing any  data. For this reason, miners can expect to donate an amount of storage to the network that is linearly proportional to the amount that they use. This is approximately equal to the amount of data they use plus the redundancy rate defined by the protocol.

### Stakeholder Motivations

in this section I will offer a description of the motivations of both the miners and patients, as well as the consequences of critical actions/inactions of both.

#### Miners

Just as is commonly the case in current systems, miners are financially incentivised to store patient data on the network, either through government or private funding. However, they must also *donate* an amount of storage to the network proportional to the amount they use. Therefore they cannot spam the network with data as to do so would also require them to donate large amounts of storage to the network, an unfeasible task that would ultimately negate the affects of their intentions. Miners will also need to periodically check that chunks they have stored on other branches are still accessible and that the miner is returning data upon request.

Miners have no immediate incentive to release foreign data upon the request of another branch requesting. However, nodes that are uncooperative in this way will not pass the verification check of any other nodes and will therefore not have any of their chunks accepted to the network. Therefore the miner will in effect only be able to store foreign chunks of other miners on their blockchain whilst receiving nothing in return. Additionally, with enough failed verifications, they will eventually be blacklisted by most other miners on the network. Like many decentralised networks before it, the Medilanac network relies on the assumption that the majority of branch owners intend to cooperate, and can handle a certain threshold of uncooperative nodes.

#### Patients

Patients have the choice of which miner to select to store their data. As each branch offers a near identical service, and mobility of data is high, service prices will remain competitive. Many branches will offer incentives such as discounts in return for de-anonymisation of certain medical information, which could be used for research. Governments could set up multiple branches and provide the service for free. With either case, it is at the discretion of the user to decide where to store their data.

All patient data uploaded to the network will be visible to all parties; this is required in order to validate the data with regards to the hashes on the blockchain. Therefore patients will be required to encrypt any private medical data. Patients will be able to easily upload any data to the network unencrypted or share read-only keys with specific parties should they wish to donate personal data for research purposes.

### Implementation Dependent Designs

There are a number of design decisions that must be addressed when implementing the protocol as there are a number of parameters and design variants that can be included or excluded based on the objectives and limitations of the scenario. In this section I will outline examples of such design variants and discuss situations in which they might be more and less suited.

**Parameters**

The most important thing to consider when implementing the protocol is the parameters that are specified for data on the network. This minimum and maximum block sizes should be selected carefully. A protocol that imposes smaller block sizes could perhaps be designed for use with mobile devices storing backups of data on the cloud, where as networks implementing a larger maximum size could be better suited to the sharing of medical data between hospitals, as it allows for heavier data storage but simultaneously increases the barrier to entry to the network. The amount of data redundancy that is specified by the network is also a factor that should be carefully considered. More data redundancy means that the network has a higher fault tollerance and lower risk of data loss. However, a high data redundancy rate also requires more storage to be *donated* to the network with each block, again increasing the barrier to entry for miners.

**Multi-linked Blockchain**

Conceptually similar to a multi-linked list, a multi-linked blockchain decrees that block store the hashes of multiple previous blocks, as opposed to just the one previous block. In this way, the blockchains robustness to data loss is strengthened as each block is not reliant on every prior blocks reconstruction. This is because, in the event of a loss of a block from the network, the hash stored in the subsequent block can validate the block prior to the block that cannot be reconstructed. Whilst the data containing within the block that could not be reconstructed is indeed lost, it is still possible to verify the data in subsequent blocks and the blockchain can be continued to be reconstructed.

**Permissions**

There are a number of issues that must be considered when deciding on a protocol for how miners store data on each blockchain. As the network necessitates that all data on a blockchain must be able to be freely shared by miners, upon request, to any party, the risk of loss or theft of encryption keys used to encrypt private medical data could have quite disastrous consequences. As the blockchain is an append only data structure, the keys used to encrypt data cannot be changed/altered. Therefore a malicious actor who gets possession of a key then has access to all data that it was used for on the blockchain. If a malicious actor gains possession of a key used to sign data for a particular blockchain then they are also able to update information in the medical record.

The consequences of this risk can be mitigated through implementing measures such as using different keys for each file and allowing for permissions to be stated within the record itself for different keys. The protocol can also implement a *termination flag* that can be appended to any record on the blockchain, informaing all participants to not accept any further data on said record. In this way, should an attacker steal a key used to sign data that is added to a medical record, the victim is able to invoke this flag (which cannot be removed again by anyone) terminating the record. The user can then create a new record on the blockchain, linking to the previous medical record, at a specified point in time, hence undoing the damage cause by the malicious actor. This approach involves no additional security of privacy risks as the data in the record remains unreadable to anyone without the key. Therefore, a malicious person trying to claim another's medical record as their own would have no use for the record as it remains encrypted with keys they do not possess.

## Implementation

The implementation of the Medilanac network protocol consists of a simulation of the different components and stakeholders of the network. The system incorporates all of the relevant security features to make it as robust as a deployable version of the network would be. The simulation is able to span across multiple different machines on multiple different networks. This is important as the original algorithm will most likely be implemented on top of the TCP/IP layer of the Internet. Therefore a working simulation that incorporates technologies that already exist offers a stronger proof of implementability.

I decided to build most of my system in Python for several reasons. Firstly I have some experience with Python, therefore the learning curve with regard to getting started on this project was less steep than it otherwise would have been If I were to use a network simulation framework that I had no experience in. Secondly, although the learning curve was less steep with Python, I preempted that this project would also require gaining a great deal of experience with a number of libraries, regardless of the approach. I therefore decided that gaining experience with a variety of commonly used libraries would be more beneficial to my personal growth than experience with fewer/less widely used packages. Finally, i chose Python specifically because of the wealth of open source libraries available, allowing me to spend less time working on parts of the software that lack in innovation, such as the implementation of encryption algorithms, and more time producing a design that meets more of the criteria of the goal of the project.

The end product implements all of the core security and validation functionalities that a miner on a productionised version of the system would implement. The miners verify signatures and hashes where appropriate, as well as execute a miner validation process with every chunk exchange. However, the validation process undertaken by the miners in rather minimal and would likely be more rigorous in a productionised version of the network.

### Modules

The blockchain generation modules will consist of simulated miners, a miner address exchange and a data reconstruction script. The miners simulate the role of the branch owners in building and signing the blockchain. The exchange facilitates the peer discovery of the different miners, allowing for the peer-to-peer sharing of chunks between branches. The reconstruction script serves as a demonstration of the process that patients would follow if they were to lose access to the branch containing their data.

#### Miners

Each miner runs two processes, one is the primary process in charge of generating the blockchain, including fetching foreign chunks, collecting primary data from patient modules, and formatting the data onto the blockchain. The second process is for a web server that listens for requests of other miners and returns chunks/data as required. The two processes use process locks to handle the parallel processing data and communication between each other. 

The different miner process all run independently from one another on the same or multiple computers, with no shared memory. Therefore all communications between miners come in the form of requests from one miners primary process being sent to another miners server process. The miners collect data generated by patient objects that symbolises the medical data being added to medical records on the network by patients. A copy of the block is encoded into chunks using the Reed Solomon Erasure Coding protocol. These chunks are then distributed to other miners.

**Primary Process**

The primary miner process executes a loop that generates a new block with each iteration. The process of generating a new loop begins with the initialisation of the block object and the gathering of sample data from a set of patient objects. The block header section is updated with a merkle tree of all the data that will be in the block. Data is added to the block to include information about the branch and miner it originates from, as well as information linking it to the previous block on the chain. Next, foreign chunks are gathered from other miner server process on the network. Thee process of gathering a chunk consists of validating and then requesting a chunk from a miner that is randomly selected from the list of miners on the network obtained from the exchange. The validation process consists of querying a miner for the headers of the entirety of their blockchain, a file is the randomly selected and then requested from the miner. The returned file is then hashed and compared to the hash in the merkle tree. If they are equal, and the blockchain headers that were returned from the miner are valid, the miner is successfully validated. Once all foreign chunks have been retrieved, the foreign chunk merkle is added to the block and the block. The block is the encoded using erasure code into chunks and headers information is added to the chunks including data that identifies the source branch and miner, along with a digital signature. These chunks are then written to file.

**Server Process**

The server process is continuously listening for requests from other miners. Upon receiving a request for a chunk or block, the process will acquire the process lock shared with the primary miner process. Next, the process will acquire the thread lock that is shared between all threads on the same miner server process. This is required as all requests to the server trigger the creation of a new thread so as to handle each request concurrently. After acquiring the process and thread locks, the chunks/blocks are read from file and the locks released. The data will then be returned to the requester and if necessary, the chunks on disk will be updated after reacquiring the process and thread locks.

#### Exchange

The exchange only listens for two types of request from miners. The first is used by miners to publish their existence upon initialisation. The miner public key and address are passed to the exchange in the body of the request. The second type of request is a retrieval of the list of all miners that the exchange is aware of along with their respective urls.

The exchange implements no validation or security measures leaving it open to many attacks such as spam of denial of service. Measures to prevent such attacks have not been implemented as part of this project as the exchange serves its purpose without such requirement. That is, the exchange represents a method of peer discovery, an area of the system concept that is left with minimal design. This is because it is an area that will be dependent on the implementation rather than the network protocol. The distinct lack of server-side processing on the part f the exchange also demonstrates the ability of miners to chose which branches they want to accept chunks from.

> TODO: reword ^

#### Patients

The patient modules generate data to be stored on the blockchain. The data is in the form of example medical data files. The files are encoded into base64 and stored as ascii data on the blockchain. For this simulation, the miner objects initialise a predefined number of patient objects and load data from them. The miner will then verify the signature so as to ensure authenticity and acceptance by other miners on the network.

Currently the data consists of example health data files that are encoded into base64 and then stored as ascii data on the blockchain. With further development, the data could be stored as standardised data records that will conform to a given schema. A schema used in a production implementation of the system would require extensive collaboration with medical professionals in order to produce a schema that accommodates enough variance of data whilst not impeding on medical research through poorly formatted datasets.

#### Branch Reconstruction

Currently a branch reconstruction program demonstrates the process that would be followed by a patient or group of patients if they were to lose access to any given branch. The program queries data in the blockchain files in the relevant directories for foreign chunks from a given branch. The program then reconstructs the primary data of each block using the chunks by following the Reed Solomon Erasure Coding reconstruction algorithm. All primary data on branches is ignored. The module sorts all chunks found pertaining to the desired branch using information in each chunk header and then reconstructs the original data.

### Results

Below is the sanitised log of a minimalistic simulation with 3 miners generating two blocks each (not including the uniform genesis block).

```
No warnings from config validation
No errors from config validation
Miner 2: Initialised. PubKey hash: 2cd29f97..
Miner 0: Initialised. PubKey hash: 510a0fa4..
Miner 1: Initialised. PubKey hash: e93f93d9..
Miner 0: Chunks found: (5/5) (510a0fa4)
Miner 1: Chunks found: (5/5) (e93f93d9)
Miner 0: Added block 1 to chain
Miner 1: Added block 1 to chain
Miner 2: Chunks found: (5/5) (2cd29f97)
Miner 2: Added block 1 to chain
Miner 1: Chunks found: (5/5) (e93f93d9)
Miner 1: Added block 2 to chain
Miner 1: Terminated with 1 chunks left to publish
Miner 0: Chunks found: (5/5) (510a0fa4)
Miner 0: Added block 2 to chain
Miner 2: Chunks found: (5/5) (2cd29f97)
Miner 0: Terminated with 0 chunks left to publish
Miner 2: Added block 2 to chain
Miner 2: Terminated with 2 chunks left to publish
```

First each miner generates a genesis block that has some standard data as well as the branch owners public key. The miners then begin generating some primary data for their first block. This data is a randomly generated 64 character string. The block head and primary data is then used to generate 5 chunks. These chunks are then published to the exchange and downloaded by other miners. The miners add these (now foreign) chunks to their blockchains and execute the same process to generate another block.

Below is an example of a blockchain with only a genesis block and one standard block. The standard block contains one file,  and only one foreign chunk is displayed.

```json
[
    {
        "body": "This is the genesis block, the first block on the blockchain",
        "head": {
            "chain_id": "510a0fa4227bcb57b474e884ce6e2d82b2504fd10626be7dda9a7de2f6bd..",
            "id": 0,
            "pub_key": "2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d49494.."
        }
    },
    {
        "body": "v7NiEvaxDZDlwK8WKVr6Yu38RgNSNg80JFwrrLtuNUEvMdyMOEjqyYaaJhCbDUgSjaa6..",
        "foreign_chunks": [
            {
                "data": "2336a516c707372506a77386559786d6d5361374161585153376c5341483..",
                "hash": "d7c67396bbe9e542b76735d621c7b088b0d39ccab119b328a2a60ce46dde..",
                "head": {
                    "block_id": 0,
                    "chain_id": "e93f93d96262c0fe22e0c3c2186589cbfc287eabf4b344536b9c..",
                    "chunk_id": 2
                },
                "signature": 7316618108853291819529610606802359618613625971406828120019..
            }, ..
        ],
        "head": {
            "chain_id": "510a0fa4227bcb57b474e884ce6e2d82b2504fd10626be7dda9a7de2f6bd..",
            "chunk_merkle": [
                [
                    "620e8d5e46ea00d09a1b751ce7168a692e1a28512a2792179e4811086dfdb345"
                ],
                [
                    "0f9c03ec5fe222268bc26f5cdfe81d8ffd8ce263009f78afec6b71056df7d4e9",
                    "8fe21d616a894ccca9ff1cde7fd4c9aa225ddd73d3bbea1bc2698ba2a517bce6"
                ],
                [
                    "d2f4e250473ed5ebf40b443325e4a16ac2761402a1de4f7277ddba5e856272a9",
                    "c72e5261b0f6dd38af23c2e66c542822bdb79bc94a211c41448713167713eda7",
                    "8fe21d616a894ccca9ff1cde7fd4c9aa225ddd73d3bbea1bc2698ba2a517bce6"
                ]
            ],
            "file_merkle": [
                ["v7NiEvaxDZDlwK8WKVr6Yu38RgNSNg80JFwrrLtuNUEvMdyMOEjqyYaaJhCbDUgSja.."]
            ],
            "id": 1,
            "prev_block_hash": "275953b8ac5259a2fdb6b1773ffcb02193987f801a198f0170837..",
            "prev_block_head_hash": "d8f10ce6ff3b8380f74208149e147996b26c102726518358..",
            "pub_key": "2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d49494.."
        }
    }
]
```

The only data in each block that is not reconstructed is the foreign chunks. This is one of the limitations of the system design.

### Bugs

**Thread Recursion**

I encountered a bug where some miner server processes would intermittently freeze and make no progress with their blockchain generation. The bug arose when code in a function for reading chunks from disk was executed. The function would sometimes fail to correctly read from disk due to various operating system related issues, as well as sometimes being interrupted by the main miner process attempting to write to the same file.

My initial solution was to implement the function recursively, so that if the system call to read data failed then function would call itself and attempt to read the data again. The function had a time to live (TTL) counter included so that the stack could never grow too large and crash the program. Whilst this was effective at handling the failure due to the operating system, it was less effective at handling the issue arising from multiple processes attempting to access the same file at the same time. To combat this, I implemented a process lock that would need to be acquired and then released by any process when attempting to read or write to any shared file. As each miner is modelled to be a separate entity from any other miner, none has shared resources with other miners and therefore each miner had their own independent process lock.

The miner processes would freeze because when the process lock was implemented, the recursion was called within the critical section of the miner servers code for reading from file. Therefore, if the process failed due to an OS related reason, the miner server's function would call itself before releasing the process lock. The miner process would then deadlock waiting to acquire a lock that it already had. The solution was to ensure the release of the lock before the recursive function called itself.

**Foreign Chunks**

Another bug was discovered during the later stages of development in which each block on the blockchain was increasing in size exponentially. If the simulation was run whilst configured to generate a large enough number of blocks then the data would quickly become too large to be submitted as a http request within a reasonable timeframe.

The bug resulted from a mistake in the code which meant that foreign chunks were being included in the block that was encoded into chunks and then distributed. This meant that each block contained chunks of its previous block. The previous block however also included chunks from its previous chunk, and so on and so forth. This error disrupted the ratio of data redundancy on the network by introducing large amounts of redundant data in an unsustainable way. Whilst this technical issue was was a disruption to development, it also provided a useful demonstration for the reasons for the initial design decision to not include foreign chunks when encoding and distributing blocks to the network.

**Network Termination**

As each miner in the system is running in parallel for a finite amount of time/iterations, there fundamentally must be a first and last miner to terminate. The final miner to terminate then, will be attempting to distribute, and potentially also gather chunks to/from a network with no other active miners. The miner will therefore not be able to submit their chunks to the network. The miner is programmed to try a finite number of attempts to gather foreign chunks before publishing the blockchain regardless. For this reason the simulation still terminates, however a full branch reconstruction may not always be possible as some chunks from the final blocks will not be published to the network.

This issue is demonstrated in fig **XXX**. Miner 2 terminates with two chunks remaining to be distributed, however all other miners on the network have already terminated, so the chunks will fail to be added to the network.The network need only handle single miners leaving/joining at any time, which it indeed does. 

This is not a problem of the protocol as a productionised version of the software would never need to handle a complete termination of the network as the network is designed to be continuously active. The network need only handle single miners leaving/joining at any time. 

Similarly, the network can encounter problems during the initialisation period. This is because the first miner on the network cannot add a block until receiving a minimum number of foreign chunks from other miners. Therefore the network can deadlock if there is a delay between the first and second active miners on the network. This problem is less prevalent in the Medilanac system as the miner initialisation is fast.

## Testing

Unit testing is the most reliable testing method and many modules can be tested using unit testing with relative ease. Modules for cryptography, blockchain validation and merkle tree encoding are all used by multiple other modules across the system. They are all coded to be functional modules and can therefore be tested with known input/output combinations.

**Merkle Tree Module**

The merkle module tests consist of tests for all combinations of input types. The module is tested against lists of even and odd length of types `int`, `string` and `bytes`. The network protocol does not require there to be a standard oder for files, that is, medical data can be uploaded to the blockchain in any order the miner chooses. This was a deliberate design choice. As there is no necessity for data to be in any specific order for the network to function. Adding unrequired constraints to the schema of the protocol increases the complexity of the scheme and therefore the barrier to entry for miners and therefore users.

**Cryptographic Module**

All cryptographic algorithms used for this project were implemented using the pyCrypto library. This library is open source and undergoes sufficient testing outside of this project and is therefore not tested as part of this project. However, the crypto module that serves as an extra layer of abstraction for the pyCrypto module that has been written as part of this program requires testing. Some methods of the crypto module are tested using standard input/output comparisons, such as for checking that the output of the hash function for a fixed input remains consistent throughout development. Metamorphic testing has also been implemented testing the following metamorphic relations:

- The hash of two different strings should not be equal
- The message output from sequential encryption followed by decryption of a message should be equal to the original
- When encrypting the same message with two different keys, the ciphertexts should not be equal.
- When encrypting two different messages with the same key, the ciphertexts should not be equal.

**Blockchain Validation Module**

Because the blockchain validation module must be able to be replicated on multiple machines across the network, it can be unit tested in a similar way to the cryptographic module. Therefore the validation algorithm can be tested by passing in a series of valid and invalid blockchains and comparing the output to the known validity of the blockchain.

The mechanism (oracle) for determining the validity of each blockchain used as a test case is fundamentally the software itself under the supervision of the developer. That is, the valid blockchains were generated using a version of the software that was judged to be correct. These valid blockchains were then either directly used as valid blockchains in test cases, or altered in some way as to make them invalid and used as invalid blockchain test cases. Using the output of a previous version of the software as an oracle for the later versions is not an ideal approach as it risks carrying unknown bugs/errors forward to the new version. However, it is the most feasible option and is still capable of flagging an unintended change to the output of the software.

### E2E

Another way to test the software is by running an end-to-end test. The test script runs the software from start to finish with preconfigured parameters. Each branch is then attempted to be reconstructed. If any branch fails then the output of the test is also a fail. If there are any errors during the simulation, these will also trigger a failed test.

A caveat with this method of testing is that the test script ignores the final two blocks on each blockchain. This is to account for the complications and errors resulting from the termination of the software. Considder thhe following high level logical flow stages of the miner process (incomplete as some stages have been omitted):

1. Generate/gather primary data of block
2. Retrieve foreign chunks
3. Update block merkle tree
4. Generate chunks of block
5. Submit chunks to server for distribution

Note that it is not possible for each miner to generate chunks for each new block until after it has retrieved the required number of foreign chunks from other miners. This is because the merkle tree of these chunks is included in the block data, therefore the hashes of each chunk must be known before a block can be completely generated. This combined with the issue outlined in section **XXX** requires the end-to-end test script to handle this eventuality by checking that all blocks on the blockchain can be reconstructed with the exception of a given number at the end, which, in this case is set to two blocks.

As the end to end test script involves miners validating the output of other miners, the miner module has a high level of test coverage. If the output of any given miner is invalid, it should be rejected from the network by all other miners and would therefore not be able to be reconstructed, failing the test.

###Metamorphic Holistic Testing

The extent to which unit testing can be applied to the Medilanac program is limited. This is because many modules of the software rely on fetching and receiving data from a server (simulating a different miner). Therefore the process of designing and building a test harness that simulates a miner for the test module to interact with is not feasible within the time constraints of the project. Therefore alternative testing methodologies must be applied in order to ensue good test coverage of the software.

Metamorphic testing is a way of testing software in which tests do not compare a set of inputs against an expected output, but rather analyse relationships between multiple input-output pairs [15]. The following metamorphic relationships are expected to hold true and can therefore be tested:

- Average bytes stored per branch should remain constant when varying the number of branches/miners on the network.
- The resulting blocks created by any combination of chunks originating from the same block should all be equal.
- Foreign chunks accepted onto one branch should not be rejected from another.
- The fault tolerance should be mathematically related in some (currently unknown) way to the recovery ratio of the erasure coding code rate.

> TODO: update with results ^

I have decided to focus on testing the relationship between the fault tolerance of the network and the level of data redundancy that is implemented on the network. I have chosen this metamorphic relationship as I believe it to be the one that offers the best test coverage and will yield the most interesting results.

### Reconstruction fault tolerance

In order to investigate how the fault tolerance of the network is related to the data redundancy introduced using erasure coding, several simulations were undertaken with data collected about each one. The simulation involved multiple complete runs of the software, each with 50 miners generating six blocks on the blockchain. However, with each subsequent run of the simulation, the ratio of the k to m was changed in order to vary the amount of data redundancy.

As the network is more susceptible to being affected by the quantity and timing of interactions between miners, rather than the amount of data within each interaction, the value of m remained at a constant value of 10, and only the value of k was altered.

With each simulation, 20 miners were then chosen at random to be tested out of the 50 miners participating in the network. The test involved the sequential removal of branches from the network, testing to see if the branch belonging to the miner under test can be successfully reconstructed from the rest of the branches still present. This was continued until the branch can no longer be reconstructed. The number of branches that have been removed is then recorded and the next miner to be tested was selected, with all previously removed branches returned to the network. The reconstruction of the branch needed to successfully reconstruct the first 4 blocks on the blockchain only in order to pass the test. This is to account for any chunks that are missing on the network resulting from the termination of the simulation, as outlined in section **XXX**.

![ft_results](Diss.assets/ft_results.png)

We can see from the results that the network fault tolerance increases linearly with data redundancy. This is to be expected as with a higher degree of data redundancy, fewer chunks must be sourced to reconstruct each block. We can also see however, that the gradient is less than 1. This is resulting from the criteria required for a reconstruction to be classed as successful. We defined a successful branch reconstruction as being able to reconstruct all blocks on the branch (with the exception of the final two which are not considered). Therefore, the probabilities of each individual block being successfully reconstructed must be multiplied in order to obtain an estimate for the probability of the branch being successfully reconstructed. Hence it is hypothesised that the relationship between fault rate and the number of blocks generated will be non-linear. It is possible to introduce an effective increase in fault tolerance by designing each blockchain such that they store hash links to multiple previous blocks, as opposed to just one, as outlined in section **XXX**.

The benefit of an implementing a high data redundancy rate is clear, each miner/user can cope with a higher number of nodes failing before losing the ability to recover data. However this directly affects the amount of data that each node is required to *donate* to the network. If the data redundancy rate is too high, the network will become inefficient and the barrier of entry will increase costs to miners/users.

### Malicious Miner

> TODO? Build a subclass of the miner class that does not store and data and attempts to free-ride on the network, add the output of the miner showing how none of its blocks are added to the network.

### Storage Proportion of Each Block

Analysis was conducted into the storage efficiency of each block with varying sizes of primary data. By analysing the ratio of the amount of primary data on a block to the total size of the block, we can get an idea of how efficient the network is at storing data whilst ensuring a sufficient backup of the data.

The data was gathered by running the simulation multiple times. With each run, the only parameter that was altered was the size of the primary data that was being stored on each block. The size of the primary data affect the size of the data within each chunk, given the fixed value of K and M used for the erasure coding. Therefore understanding the relationship, between the size of the primary data and its affect on the chunk requirements is useful in analysing how the network would fair against heavier storage requirements.![BlockSize_v_PrimaryDataSize](Diss.assets/BlockSize_v_PrimaryDataSize.png)

![DataRatio_v_PrimaryDataSize](Diss.assets/DataRatio_v_PrimaryDataSize.png)

As can be seen in figure **XXX**, the total size of each block grows linearly with the size of the primary data that is stored on each block. This is fundamentally because the erasure coding algorithm used to incorporate data redundancy do so by producing an amount of redundant data that is linearly related to the size of the original (primary) data. Therefore, the size of each block is approximately equal to the size of the primary data multiplied by the rate of data redundancy, plus the size of the block headers.

As, for the most part, the block headers remain at a fixed size, the ratio of block size to primary data size decreases exponentially as the size of primary data stored on each block increases (figure **XXX**). This means that the network becomes more efficient with an increase in block size, but with diminishing returns. This relationship is significant because it defines the amount of additional data each node is required to store when adding their own data to the network, an amount that should therefore be minimised as much as possible. When defining the maximum block size for a productionised version of the network, consideration must be given to the tradeoff between storage efficiency and other real world constraints such as the resulting minimum storage requirements of nodes.

The most efficient data storage achieved during testing was an overall storage requirement of 350% of the primary data being stored. This simulation used 2 and 3 for the values of k and m respectively. Therefore we can assume that 150% of the additional data requirement was used for data redundancy, with the remaining 100% being attributed to the overheads of the data requirements of using blockchain. This includes header information of the block such as public keys, and hashes, as well as header information for each foreign chunk.

## Further Developments

In this section I will discuss further developments that could be made to this software that are outside the scope of this project.

#### Blockchain Data Format

With additional time, I would like to have developed a data format that does not rely as heavily on JSON. The reason being that it is generally not good practice to store files as ascii data as it is a relatively inefficient method of storage. Although sufficing for this project, complication arise when large files are required to be stored on the blockchain. As the data is stored in JSON format, the entire blockchain must be parsed in order to load the data. As previously mentioned, this can be mitigated by splitting each block up into its own JSON file, however this is still not a complete solution in an implementation where blocks are gigabytes or even terabytes big. Instead I would implement a design such that each block was a zip archive such that each file could remain in its original form, storing only the block headers as ascii data. The merkle tree in the block headers would then link to either the files themselves, or even a uniform size of fragment of each file in order to speed up the miner validation process that is carried out with each exchanging of chunks.

#### Security Features

Additional security measures could be added to the verification process of miners. In a productionised version of the system, this would likely be a process that would be continuously updated. Security measures such as a miner blacklist that miners who fail the verification process are added to.

> TODO: Additional security features

#### Miners scanning network

An additional development for the system could be the implementation of an additional role of the miners that has not yet been explored. In a productionised version of the software, miners may wish to periodically check that all chunks that they have distributed out across the network are on branches that are still functional and active. This is because, in the event of a loss of a chunk from the network, the threshold of data redundancy for the block is relates to is in effect reduced. Miners therefore may wish to redistribute chunks to the network that have been lost, in order to ensure the data is properly backed up to the network.

A similar development would be the addition of signatures and addresses of the locations of where a miners foreign chunks are stored on the network. This information could be stored in subsequent blocks, further increasing the transparency of the network, as well as the ease of data reconstruction in the event of a miner failure.

#### System Vulnerabilities

Two weaknesses of the network design came to light during development. The first was that lack of capability for handling a malicious miner that attempts to store multiple copies of each of their chunks on the network. A miner may wish to do this in order to increase the number of copies of their data on the network and therefore the fault tolerance of the network with respect to their data. Storing multiple copies of chunks is an inefficient way of increasing the data redundancy and would have a negative effect on the network as it would alter the ratio of primary to secondary data that each miner must store. A miner that was compliantly storing foreign chunks on their blockchain could distribute multiple copies of their own chunks. This would go largely undetected as the only way to discover that this attack has been carried out by any given miner would be to scan the entire network, querying for multiple copies of the same chunk. This would likely be an unfeasible task to regularly perform on networks of considerable size. However, it is worth noting that only the query could be executed on blockchain headers only, querying for specific hashes of chunks.

The second vulnerability arises when a malicious miner adds to a block a merkle tree that has been specifically designed so that the seed data can be generated when needed, rather than stored. Whilst conceptually unproven, it has been hypothesised that it is possible to generate a merkle tree for data that has been fabricated using an algorithm that produces data indistinguishable from encrypted files. The data is generated in such a way that specific sections of the data can be easily re-generated when required. This would allow a miner to appear to other miners on the network to be storing vast amounts of data, whilst in reality it is generating the specific sections of data required in order to pass the miner validation checks associated with adding chunks to foreign branches. Further research into the aforementioned areas is therefore required in order to combat the vulnerabilities.

#### Nodes leaving and rejoining

Traditional blockchain technology can cope with nodes leaving and rejoining the network exceptionally well. This is because the complete blockchain is stored on all nodes [2]. Therefore, nodes can simply query another node upon rejoining. However, the system laid out above was designed so that this is not the case. Therefore it currently has very little tolerance for nodes wishing to leave, as data they were previously hosting must be reconstructed and new primary storage must be set up. Further research could be undertaken to establish a way in which node are able to leave and rejoin the network.

## Reflection

Overall I am pleased with the outcome of the project. Throughout the project I utilised numerous software engineering best practices, including source control, test driven development, and agile methodologies. The program has been written to produce extensive logs that can be effectively utilised for debugging as well as clarifying the logical flow of the program. Resultantly, the code produced is of a high quality.

As the project progressed the emphasis and motivation of the product in the medical domain has shifted marginally into a broader use case: decentralised storage of data. This is mostly because, whilst the motivation of improving both healthcare and data privacy for patients has remained unscathed, the development of the system uncovered an unexpected caveat: the protocol itself had very few design components tying it to medical data. The system could be applied to a wide range of use cases involving the need for decentralised storage of data.

In order to design a system that is build on top of blockchain, it is imperative to have a good understanding of the technology to include it's strengths, weaknesses, and vulnerabilities. Therefore a significant proportion of this project was allocated to expanding my prior knowledge in this field, and conducting extensive research into the wider and narrower domain related to subject of the project.

**Agile Methodology**

I utilised a variation of the agile methodology to produce the code and dissertation for this project. The process dictated that each sprint last a day of work, with the intended increment to the minimum viable product being defined at the start of each iteration. This aided the development of the project as it reiterated the idea that the direction and design of the system was dynamic and continuously changing. However, in future projects such as this, I will put more emphasis on high level design considderations throughout. I found with this project that it was, at times, too easy to focus too intently on the minor design details and security vulnerabilities, sometimes to the detriment of broader ones. For example, It was not until the later stages of testing the project that I discovered the defects outlined in section **XXX**. Had I placed more consideration into an overview of the system, I would have perhaps spotted this shortcoming earlier and had the opportunity to design measures to rectify it.

**Test Driven Development**

Test driven development (TDD) is a software development process where requirements are translated into test cases before the software is improved so as to pass the tests [28]. TDD was used for the areas of the project that it could be feasibly applied to without adding excessive workload to the project. TDD helped to ensure that the minimum viable product criteria was clearly defined and not exceeded for the modules it was applied to, as well as assisting in the design and specification of the API for each module.

**Setbacks**

Approximately half way through, the project had to be abruptly relocated to a different university. The decision to use source control that was sufficiently backed up in multiple locations saved the project from what would most likely have been weeks of delays and setbacks. Git also helped develop features and improvements that could easily be abandoned at a later stage, something that it crucial when working to the agile methodology.

Additionally, the relocation altered the deadline and marking criteria of the project. Resultantly the project plan had to be adapted to meet the new deadline and requirements. Throughout the earlier stages of the project, I adhered to the project plan with discipline. However, whilst remaining on schedule, I did not utilise the opportunity to get ahead of schedule. In the future I would put more emphasis on remaining ahead of schedule in order to maximise the slack time available for unforeseen setbacks.

#### Technical Development

The decision to use Python and various individual libraries for the development was a success overall. I believe that the learning curve was more gradual than it would have been had I taken other, more framework heavy, routes such as using NS3. This route also enables the experience gained to be varied over a broader range of technologies to include multiprocessing, web servers, encryption, erasure coding. I believe the experience gained with this array of more general technologies will be more beneficial than more in-depth experience with a single, less widely used framework.

## Conclusion

Previous works in this domain include the design of systems that utilise blockchain for the permission definition of data stored off-chain, and the combination of erasure coding with blockchain to reduce the storage requirements for certain nodes. The Medilanac system is the first design to store data on the blockchain whilst maintaining reasonable storage overheads, as well as combining erasure code for the purpose of fragmenting blocks for distribution across the network. This innovation is crucial in order to avoid storing data in a standard data centre that must be trusted by the user, leaving the user open to malice or incompetence on the part of the data storage service provider.

I have implemented a working simulation of miners adding medical data to a blockchain and sharing chunks of their blocks with one-another. I have written software capable of reconstructing the primary data on any one branch from secondary data on different branches on the network, and have demonstrated the effectiveness of this software given the failure/loss of a branch of data. Testing of the software revealed that the overheads of the network amount to approximately 150% of the primary data being stored which, while significant, is a reasonable cost for the benefits provided by a trust-less peer-to-peer data storage platform.

The majority of the core security features of the network have been implemented, however the simulation still lacks some features that leaves it vulnerable to certain attacks. That being said, the program has successfully fulfilled the aim of the project: to demonstrate the proof of concept of the algorithm.

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
26. Luc Wood, Accredited Osteopath, Interview
27. Zohar, Aviv. "Bitcoin: under the hood." *Communications of the ACM* 58.9 (2015): 104-113.
28. https://en.wikipedia.org/wiki/Test-driven_development

