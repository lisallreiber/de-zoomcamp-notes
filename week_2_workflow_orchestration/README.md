Week 2: Workflow Orchestration <!-- omit from toc -->
------------------------------


- [2.1 Data Lake](#21-data-lake)
  - [2.1.1 - Data Lake (GCS)](#211---data-lake-gcs)
- [2.2 - Prefect](#22---prefect)
  - [2.2.1 - Introduction to Workflow orchestration](#221---introduction-to-workflow-orchestration)
  - [2.2.2 - Introduction to Prefect concepts](#222---introduction-to-prefect-concepts)
  - [step01: add prefect flow and task](#step01-add-prefect-flow-and-task)
  - [step02: add prefect task](#step02-add-prefect-task)
  - [step3: parameterizing the flow](#step3-parameterizing-the-flow)
  - [step 4 Prefect Orion (UI)](#step-4-prefect-orion-ui)
  - [step5: blocks and collections](#step5-blocks-and-collections)
    - [step 5.1 postgres connector block](#step-51-postgres-connector-block)
  - [2.2.3 - ETL with GCP \& Prefect](#223---etl-with-gcp--prefect)
  - [2.2.4 - From Google Cloud Storage to Big Query](#224---from-google-cloud-storage-to-big-query)
  - [2.2.5 - Parametrizing Flow \& Deployments](#225---parametrizing-flow--deployments)
  - [2.2.6 - Schedules \& Docker Storage with Infrastructure](#226---schedules--docker-storage-with-infrastructure)
  - [2.2.7 - Prefect Cloud and Additional Resources](#227---prefect-cloud-and-additional-resources)
- [Code repository](#code-repository)
- [Homework](#homework)
- [Community notes](#community-notes)
  - [2022 notes](#2022-notes)

## 2.1 Data Lake

### 2.1.1 - Data Lake (GCS)

* What is a Data Lake
* ELT vs. ETL
* Alternatives to components (S3/HDFS, Redshift, Snowflake etc.)
* [Video](https://www.youtube.com/watch?v=W3Zm6rjOq70&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
* [Slides](https://docs.google.com/presentation/d/1RkH-YhBz2apIjYZAxUz2Uks4Pt51-fVWVN9CcH9ckyY/edit?usp=sharing)


## 2.2 - Prefect

### 2.2.1 - Introduction to Workflow orchestration

* What is orchestration?
* Workflow orchestrators vs. other types of orchestrators
* Core features of a workflow orchestration tool
* Different types of workflow orchestration tools that currently exist 

:movie_camera: [Video](https://www.youtube.com/watch?v=8oLs6pzHp68&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=16)


### 2.2.2 - Introduction to Prefect concepts

* 00:00 What are the contents of the ingestion script?
* [01:45](https://www.youtube.com/watch?v=cdtN6dhp708&t=94s) What is Prefect?
  * Using python to write workflows
* [02:00](https://www.youtube.com/watch?v=cdtN6dhp708&t=120s) Setting up a virtual envionment with conda
* [02:50](https://www.youtube.com/watch?v=cdtN6dhp708&t=170s) Installing Prefect and Requirements
* [03:30](https://www.youtube.com/watch?v=cdtN6dhp708&t=210s) Recap: 'ingest_data.py' and pgAdmin
* [05:10](https://www.youtube.com/watch?v=cdtN6dhp708&t=310s) Why a scheduler is useful: transforming the script into a flow
  
  - positive effect of scheduler is being able to run the script at a specific time, get resilience
  - thats why we will transform the script into a prefect flow

### step01: add prefect flow and task 

  * [05:55](https://www.youtube.com/watch?v=cdtN6dhp708&t=355s) Prefect flow: What is it and how to add it?

  A prefect flow is the most basic python object. It acts as a container of the workflow logic. You can interact with it and it helps to unserstand the workflwo of a project. It it similar to a function: they take inputs, perform work and create outputs. Flows are incorporated in python scripts with an `@flow` decorator above the main function. 
  
  Conceptually, a flow is a collection of tasks that are executed in a specific order. The flow is the main object that we will use to run our tasks. We can add tasks to the flow by using the flow's `@task` decorator. The decorator will add the task to the flow and return the task object. We can then use the task object to add dependencies between tasks.

### step02: add prefect task
* [07:00](https://www.youtube.com/watch?v=cdtN6dhp708&t=420s) Prefect task: What is it and how to add it?

Tasks are not required for flows, but they are special because they can receive metadata about upstream dependenciey and the state of those dependencies.
With tasks you can add automated retries which can be useful when interating with external import sources. 


```bash
# we run the python script with added flow and task
python ingest-data.py
```

* [08:52](https://www.youtube.com/watch?v=cdtN6dhp708&t=532s) Recap: transforming the script into a flow
* [10:15](https://www.youtube.com/watch?v=cdtN6dhp708&t=615s) Transforming the script into ETL

Now we have successfully ingested the data, but maybe we also want to clean some stuff. Therefore we are thransforming the script further into an ETL pipline.

e.g. lets remove rows with 0 passengers

as a first step we will break ingest_data funtion info a few tasks: this will add more visibility into each step of the pipeline

helpful task arguents: 
- caching with task arguments:
  - `cache_key_fn=task_input_hash`
  - `cache_expiration=timedelta(days=1)`

* [20:00](https://www.youtube.com/watch?v=cdtN6dhp708&t=1200s) Recap: creation of tasks

### step3: parameterizing the flow

since flows are function we can pass arguments into them and use them in the flow.

again we run the script again with 

```bash
python ingest_data.py
```
* [22:20](https://www.youtube.com/watch?v=cdtN6dhp708&t=1340s) Other Prefect options
* [22:25](https://www.youtube.com/watch?v=cdtN6dhp708&t=1345s) Parameterizing the flow
* [22:30](https://www.youtube.com/watch?v=cdtN6dhp708&t=1350s) Subflows

### step 4 Prefect Orion (UI)
* [25:00](https://www.youtube.com/watch?v=cdtN6dhp708&t=1500s) Prefect Orion / UI 

now we start with the UI. We will use the UI to run our flow and to monitor it.

you can start it with 

```bash
prefect orion start
```

in the video the UI is shown a bit

### step5: blocks and collections

now we will turn to prefect blocks and collections

* [27:20](https://www.youtube.com/watch?v=cdtN6dhp708&t=1640s) Blocks and collections

Block names are immutable. Because of this, you can use the block name as a unique identifier for the block. This is useful when you want to reference a block in another block. you can refer to blocks in multiple places and if you update the block, it will update in all those places at once.

collections: they are a way to group blocks together. They are useful when you want to group blocks together and run them as a group. they are pip installable and come with pre-defines packages and tasks.


#### step 5.1 postgres connector block
* [28:41](https://www.youtube.com/watch?v=cdtN6dhp708&t=1721s) postgres-connector block

Docs are [here](https://prefecthq.github.io/prefect-sqlalchemy)

The sqlalchemy block can be installed with the Orion UI or with

```bash
pip install prefect-sqlalchemy
```

What is the connector useful for? it can be used to store the postgres credentials so we don't need to pass them in the code 

Hhen the block is created in the UI, it generated the code you need to implement it in your script. for the postgres-connector it looks like:

```bash
from prefect_sqlalchemy import SqlAlchemyConnector

with SqlAlchemyConnector.load("postgres-connector") as database_block:
  ...
```

* [29:25](https://www.youtube.com/watch?v=cdtN6dhp708&t=1765s) Prefect collections
* [30:15](https://www.youtube.com/watch?v=cdtN6dhp708&t=1825s) Utilizing the SQLalchemy block

Recap: now that we have the connector: we don't need to hardcode the connection credentials anymore. we can use the connector to connect to the database and run queries.

One last time, we run the script with 

```bash
python ingest-data.py
```

* [34:15](https://www.youtube.com/watch?v=cdtN6dhp708&t=2040s) Closing remarks



* Installing Prefect
* Prefect flow
* Creating an ETL
* Prefect task
* Blocks and collections
* Orion UI 

:movie_camera: [Video](https://www.youtube.com/watch?v=jAwRCyGLKOY&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=17)

### 2.2.3 - ETL with GCP & Prefect

* Flow 1: Putting data to Google Cloud Storage 

:movie_camera: [Video](https://www.youtube.com/watch?v=W-rMz_2GwqQ&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=18)


### 2.2.4 - From Google Cloud Storage to Big Query

* Flow 2: From GCS to BigQuery



:movie_camera: [Video](https://www.youtube.com/watch?v=Cx5jt-V5sgE&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=19)

### 2.2.5 - Parametrizing Flow & Deployments 

* Parametrizing the script from your flow
* Parameter validation with Pydantic
* Creating a deployment locally
* Setting up Prefect Agent
* Running the flow
* Notifications

:movie_camera: [Video](https://www.youtube.com/watch?v=QrDxPjX10iw&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=20)

### 2.2.6 - Schedules & Docker Storage with Infrastructure

* Scheduling a deployment
* Flow code storage
* Running tasks in Docker

:movie_camera: [Video](https://www.youtube.com/watch?v=psNSzqTsi-s&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=21)

### 2.2.7 - Prefect Cloud and Additional Resources 


* Using Prefect Cloud instead of local Prefect
* Workspaces
* Running flows on GCP

:movie_camera: [Video](https://www.youtube.com/watch?v=gGC23ZK7lr8&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=22)

* [Prefect docs](https://docs.prefect.io/)
* [Pefect Discourse](https://discourse.prefect.io/)
* [Prefect Cloud](https://app.prefect.cloud/)
* [Prefect Slack](https://prefect-community.slack.com)

## Code repository

[Code from videos](https://github.com/discdiver/prefect-zoomcamp) (with a few minor enhancements)

## Homework 

To be linked here by Jan. 30


## Community notes

Did you take notes? You can share them here.

* Add your notes here (above this line)


### 2022 notes 

Most of these notes are about Airflow, but you might find them useful.

* [Notes from Alvaro Navas](https://github.com/ziritrion/dataeng-zoomcamp/blob/main/notes/2_data_ingestion.md)
* [Notes from Aaron Wright](https://github.com/ABZ-Aaron/DataEngineerZoomCamp/blob/master/week_2_data_ingestion/README.md)
* [Notes from Abd](https://itnadigital.notion.site/Week-2-Data-Ingestion-ec2d0d36c0664bc4b8be6a554b2765fd)
* [Blog post by Isaac Kargar](https://kargarisaac.github.io/blog/data%20engineering/jupyter/2022/01/25/data-engineering-w2.html)
* [Blog, notes, walkthroughs by Sandy Behrens](https://learningdataengineering540969211.wordpress.com/2022/01/30/week-2-de-zoomcamp-2-3-2-ingesting-data-to-gcp-with-airflow/)
* Add your notes here (above this line)
