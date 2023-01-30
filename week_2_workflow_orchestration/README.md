Week 2: Workflow Orchestration <!-- omit from toc -->
------------------------------


- [2.1 Data Lake](#21-data-lake)
  - [2.1.1 - Data Lake (GCS)](#211---data-lake-gcs)
- [2.2 - Prefect](#22---prefect)
  - [2.2.1 - Introduction to Workflow orchestration](#221---introduction-to-workflow-orchestration)
  - [2.2.2 - Introduction to Prefect concepts](#222---introduction-to-prefect-concepts)
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
* [05:55](https://www.youtube.com/watch?v=cdtN6dhp708&t=355s) Prefect flow: What is it and how to add it?
* [07:00](https://www.youtube.com/watch?v=cdtN6dhp708&t=420s) Prefect task: What is it and how to add it?
* [08:52](https://www.youtube.com/watch?v=cdtN6dhp708&t=532s) Recap: transforming the script into a flow
* [10:15](https://www.youtube.com/watch?v=cdtN6dhp708&t=615s) Transforming the script into ETL
* [20:00](https://www.youtube.com/watch?v=cdtN6dhp708&t=1200s) Recap: creation of tasks
* [22:20](https://www.youtube.com/watch?v=cdtN6dhp708&t=1340s) Othe Prefect options
* [22:25](https://www.youtube.com/watch?v=cdtN6dhp708&t=1345s) Parameterizing the flow
* [22:30](https://www.youtube.com/watch?v=cdtN6dhp708&t=1350s) Subflows
* [25:00](https://www.youtube.com/watch?v=cdtN6dhp708&t=1500s) Prefect Orion / UI 
* [27:20](https://www.youtube.com/watch?v=cdtN6dhp708&t=1640s) Blocks and collections
* [28:41](https://www.youtube.com/watch?v=cdtN6dhp708&t=1721s) postgres-connector block
* [29:25](https://www.youtube.com/watch?v=cdtN6dhp708&t=1765s) Prefect collections
* [30:15](https://www.youtube.com/watch?v=cdtN6dhp708&t=1825s) Utilizing the SQLalchemy block
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
