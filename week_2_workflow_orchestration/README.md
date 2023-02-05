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
    - [Goal1: Creating a flow that collects the taxi data and writes it into Google Cloud Storage (Data Lake)](#goal1-creating-a-flow-that-collects-the-taxi-data-and-writes-it-into-google-cloud-storage-data-lake)
    - [Setup](#setup)
    - [Step01: Make a flow](#step01-make-a-flow)
    - [step02: add tasks](#step02-add-tasks)
    - [step03: write out local parquet files](#step03-write-out-local-parquet-files)
  - [2.2.4 - From Google Cloud Storage to Big Query](#224---from-google-cloud-storage-to-big-query)
    - [step 1: define flow and task1: web to gcs](#step-1-define-flow-and-task1-web-to-gcs)
    - [step 2: add task 2: transform data](#step-2-add-task-2-transform-data)
    - [step 3: add task 3: write to BigQuery](#step-3-add-task-3-write-to-bigquery)
  - [2.2.5 - Parametrizing Flow \& Deployments](#225---parametrizing-flow--deployments)
    - [Goal: parameterizing a flow script](#goal-parameterizing-a-flow-script)
    - [step1: adding parameters to the flow](#step1-adding-parameters-to-the-flow)
    - [step2: how to add a subflow](#step2-how-to-add-a-subflow)
    - [Goal: deploying flows](#goal-deploying-flows)
    - [step1: Deployment via CLI](#step1-deployment-via-cli)
    - [step2: Deployment via Python](#step2-deployment-via-python)
  - [2.2.6 - Schedules \& Docker Storage with Infrastructure](#226---schedules--docker-storage-with-infrastructure)
    - [step 1: Scheduling a deployment](#step-1-scheduling-a-deployment)
    - [step 2: Flow code storage](#step-2-flow-code-storage)
    - [step 3: Running tasks in Docker](#step-3-running-tasks-in-docker)
    - [prefect profiles](#prefect-profiles)
    - [using an agent](#using-an-agent)
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

```bash
conda activate de-zoomcamp
```

```bash
pip install -r requirements.txt 
```

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
python ingest-data.py
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

#### Goal1: Creating a flow that collects the taxi data and writes it into Google Cloud Storage (Data Lake)

#### Setup

we start off with activating the de-zoomcamp environement with 

```bash
conda activate de-zoomcamp
```

then we start the prefect orion server locally with 
```bash
prefect orion start
```

Then we create a new folder for this session 

```bash
mkdir 02_gcp
```

#### Step01: Make a flow

#### step02: add tasks

#### step03: write out local parquet files

learned that I can creat multiple nested folders with the -p flag 

```bash
mkdir -p data/yellow
```


* Flow 1: Putting data to Google Cloud Storage 

:movie_camera: [Video](https://www.youtube.com/watch?v=W-rMz_2GwqQ&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=18)

In order to load the data directly into Googe Cloud Storage, we create a new project **prefect-de-zoomcamp-376713** and a new storage bucket **prefect-de-zoomcamp_2**.

then we add the gcs prefect blocks with 

```bash
prefect block register -m prefect_gcp
```

![Screenshot of Terminal Output after registerin the gcp block](../images/Screenshot%202023-02-03%20at%2015.03.12.png)


now we configure the gcs bucket and gcs credentials blocks

for the credentials we need to create a service account and download the json file.

the service account gets the roles of 
- BigQuery Admin
- Storage Admin

then we generate a JSON Key for the service account and downlaod the JSON (making sure that we don't save it in a public repo)

the content of the key is what we paste in the setup section of the prefect gcs-credentials block

once the blocks are configures in the orion UI, it gives out the code we can use to implement/use the blocks 

```bash
from prefect_gcp.cloud_storage import GcsBucket
gcp_cloud_storage_bucket_block = GcsBucket.load("de-zoomcamp-gcs")
```


### 2.2.4 - From Google Cloud Storage to Big Query

* Flow 2: From GCS to BigQuery


:movie_camera: [Video](https://www.youtube.com/watch?v=Cx5jt-V5sgE&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=19)

#### step 1: define flow and task1: web to gcs
#### step 2: add task 2: transform data
#### step 3: add task 3: write to BigQuery


### 2.2.5 - Parametrizing Flow & Deployments 

* Parametrizing the script from your flow
* Parameter validation with Pydantic
* Creating a deployment locally
* Setting up Prefect Agent
* Running the flow
* Notifications

:movie_camera: [Video](https://www.youtube.com/watch?v=QrDxPjX10iw&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=20)

#### Goal: parameterizing a flow script

parameterizing a flow means that we can pass in parameters to the flow when we run it. The parameters (color, month, year) are not hard coded anymore but can be adapted at runtime. this way one flow could have different runs with different parameters.

#### step1: adding parameters to the flow

#### step2: how to add a subflow

How we add subflow to our script. Why? It enables us to have one flow that triggers one or many other flows. Those could also be determined by parameters. It is kind of like going one extraction layer of code up. Then we have code (parent flow) that triggers other code (subflow). 

#### Goal: deploying flows

so far we have been running the flows locally. Now we want to deploy the flows to a prefect agent. This way the flows can be run on a server and not only on our local machine.

there are two ways to build a deployment. first option is through the CLI and the second option is through python. 

[Deployment Documentation](https://docs.prefect.io/concepts/deployments/)

#### step1: Deployment via CLI

we start with building the deployment:
- first we provide the path to the script and after the colon comes the entrypoint (in this case flow)
- we need to provide the entrypoint flow, because in our script there are multiple flows defined

```bash
prefect deployment build 03_deployment/parameterized_flow.py:etl_parent_flow -n "Paramerized ETL"
```

Note: make sure you are in the same directory as the file, otherwise the .yaml file will be created from wherever you are calling the function from.

e.g. this did not work ;)
```bash
prefect deployment build parameterized_flow.py:etl_parent_flow -n "Paramerized ETL"
```
the command generates a yaml file with all the meta data.

this can be adapted as needed. 

then, we can apply the deploment with 

```bash
prefect deployment apply 03
```

once the deployment is applied, we can trigger it from the CLI or from the UI (quick or custom)

in the work queues section we can see the deployment we just created, but it cannot run without an agent. 

thats why -> in the next step, we need to create an agent who will execute the deployment

an agent is a very very lightweight python process that runs on a server (execution environment) and executes the flows.

for now our agent will be our local machine. the agent then pulls the "work" from the work queue. 

summary:
- the deployment specifies which flow goes to which work queue
- the agents pick their work form the work queue.

we start the agent with 

```bash
prefect agent start --work-queue "default"
```


#### step2: Deployment via Python

### 2.2.6 - Schedules & Docker Storage with Infrastructure

:movie_camera: [Video](https://www.youtube.com/watch?v=psNSzqTsi-s&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=21)

#### step 1: Scheduling a deployment

You can schedule a deplyment in the Orion UI in the Deployments Section

Or you can schedule it in the CLI with `prefect deployment build` and a scheduling tag

- after the colon, we specify the entrypoint flow
- `-n` tag: naming the deployment
- `--cron` tag: setting the schedule with cron
- `--interval` tag: setting the schedule with an interval
- `-a` tag: building AND applying it right away

```bash
prefect deployment build flows/03_deployment/parameterized_flow.py:etl_parent_flow -n "Paramerized ETL from CLI" --cron "0 0 * * *" -a 
```

this means we can create the schedule when we create the deployment. Keep in mind that there needs to be an agent to run the flow

#### step 2: Flow code storage
??

#### step 3: Running tasks in Docker

1. make a dockerfile with where we geth the prefecthq docker image
2. copy a docker-requirements.txt over
3. install requirements
   - use `--trusted_host` pypi.python.org 
   - use `--no-cache-dir` so that pip doesnt use anything cached
4. copy flows folder to `/opt/prefect/flows` (this is the default prefect directory for flows)
5. copy data folder ofver to default dest `opt/prefect/data`
6. build docker image with 
  ```bash
  docker build -t lisareiber/prefect:de-zoomcamp .
  ```
7. Pushing it to docker hub
   - if you are not logged into docker hub -> use `docker login` to do so
   - push with:
   - 
```bash
  docker image push lisareiber/prefect:de-zoomcamp
```
  - now its available for others 
  - if we want to use this for our deployment, we can do this with a prefect block
8. create a docker block 
  - either in the UI or in a dedicated [python file](blocks/make_docker_block.py)
9. create a deployment with the docker block
  - create a [`docker-deploy.py`](flows/03_deployment/docker_deploy.py) script where you define the flow to run and the docker image in which to run it (infrastructure argument)
10. run the docker-deploy file with
    
```bash
python flows/03_deployment/docker_deploy.py
```

#### prefect profiles

you can list them with:

```bash
prefect profiles ls
```

if you want the dockerhub container to be able to interface with orion server, you need to add the prefect api url in the prefect profile of your choice

```bash
# use a local Orion API server
prefect config set PREFECT_API_URL="http://127.0.0.1:4200/api"

# use Prefect Cloud
prefect config set PREFECT_API_URL="https://api.prefect.cloud/api/accounts/[ACCOUNT-ID]/workspaces/[WORKSPACE-ID]"
````

this way will not not use the local xxx API token. Instead we want to use an endpoint from a specific URL. Find more info in the prefect documentation

> The PREFECT_API_URL value specifies the API endpoint of your Prefect Cloud workspace or Prefect Orion API server instance. 

#### using an agent

now we start an agend with 

- `-q` flag defines the queue from which the agent takes on work

```bash
prefect agent start -q "default"
```

```bash
prefect deployment run etl-parent-flow/docker-flow -p "months=[1,2,3]"
```

What is new now, is that beforehand, everything ran on our local machine. But now, everything runs in a docker container.



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

### 2022 notes 

Most of these notes are about Airflow, but you might find them useful.

* [Notes from Alvaro Navas](https://github.com/ziritrion/dataeng-zoomcamp/blob/main/notes/2_data_ingestion.md)
* [Notes from Aaron Wright](https://github.com/ABZ-Aaron/DataEngineerZoomCamp/blob/master/week_2_data_ingestion/README.md)
* [Notes from Abd](https://itnadigital.notion.site/Week-2-Data-Ingestion-ec2d0d36c0664bc4b8be6a554b2765fd)
* [Blog post by Isaac Kargar](https://kargarisaac.github.io/blog/data%20engineering/jupyter/2022/01/25/data-engineering-w2.html)
* [Blog, notes, walkthroughs by Sandy Behrens](https://learningdataengineering540969211.wordpress.com/2022/01/30/week-2-de-zoomcamp-2-3-2-ingesting-data-to-gcp-with-airflow/)
* Add your notes here (above this line)
