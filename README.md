# Kafka-Airflow-CS777
Kafka and Airflow implementation for CS 777

## Introduction
Apache Kafka is an open-source distributed streaming system used for stream processing, real-time data pipelines, and data integration at scale. 

Apache Airflow is an open-source platform for developing, scheduling, and monitoring batch-oriented workflows.

## Environment
There are 3 major components required for implementing a Kafka-Airflow pipeline:
1. Kafka and Zookeeper
2. Docker
3. Airflow

### Setup
1. Kafka and Zookeeper

ZooKeeper plays a critical role in a Kafka cluster by providing distributed coordination and synchronization services. It maintains the cluster's metadata, manages leader elections, and enables consumers to track their consumption progress.

We start by downloading Apache Kafka and Zookeeper's binary files from the [Official Website](https://kafka.apache.org/downloads).
Extract the downloaded file to a folder.

Create two folders for saving zookeper logs and kafka server logs.

Go to the kafka folder, navigate to config/zookeeper.properties and modify the following attributes in the file to setup zookeeper:
1. dataDir= Give the path for the folder created for zookeeper logs.
2. clientPort: Specifies the port number at which the zookeeper service will run at. Default port is 2181.
3. maxClientCnxns= This property limits the actions from a host to a single zookeeper server. Default value is 0. We change it to 1.

   

Similarly, open server.properties in the same folder and modify the following attrivutes in the file to setup kafka server:
1. listeners= This property is commented by default and we need to uncomment this to specify on what ports the listeners will listen at.
2. log.dirs= Give the path for the folder created for kafka logs.
3. zookeeper.connect= Specifies the address for the zookeeper service. Default is localhost:2181
4. 
