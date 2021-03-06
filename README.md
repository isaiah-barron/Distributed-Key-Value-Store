# Distributed-Key-Value-Store

This will be a three phase project written in python that implements a distributed key-value store using Docker containers to store key-value pairs on multiple nodes/machines. Each phase will build on top of each othe, where the third phase will be the final product. 

## GOALS

To demonstrate proficient use of:
 - Distributed System Concepts
 - Docker
 - Python
 - Multithreading
 - Flask RESTful API
 
 ## Phase 1
 
 The purpose of this phase is to create a multi-site key-value store without distribution. The goal of this phase is to show that the basic functionality of
 the key/value store works properly and to familiarize myself with the basics of Docker, Flask, and web requests.
 
 Phase 1 deliverables:
 
 - create a docker container
 - create a key/value store
 - key/value pairs will be stored in memory (no persistant data)
 - build functionality to insert, update, delete, and get a value of an existing key
 - build funtionality to handle web requests (GET, PUT, DELETE)
 - Main instance and Follower instance roles for multi-site coordination. (This will prepare me for phase 2 where I will implement a partitioning mechanism into my Distributed Key-Value Store)
     - Main instance will be the node that directly responds to the client
     - Follower instance will be the node that acts as a proxy between the main instance        and the client
 
 ## Phase 2
 
This phase will focus on creating a distributed key/value store that stores key/value pairs on more than one machine/node by partitioning the key-value pairs into shards (scalability). The partitioning mechanism I will be using is Hashing which allows for uniformity, cheap reads, cheap writes, and scalability. (In the future, once I have finished all three phases, I plan on implementing Consistant Hashing. This mechanism allows for stability plus all the features that Hashing provides)
 
 Phase 2 deliverables:
 
 - Run as a collection of nodes where each node can handle a request and respond to the client
 - partition key-value pairs into shards where each node holds one shard (no replication, that will come in Phase 3)
 - The size of the shards (the count of key-value pairs in the shard) will be equal in size if and only if the number of key-value pairs are even
 - the ability to see how many key-value pairs are stored on a node
 - the ability to add new nodes (view change) and re-partition the key-value pairs into new shards (reshard) 
    - note: the key-value store will not reshard automatically
 
 ## Phase 3 (coming soon)
