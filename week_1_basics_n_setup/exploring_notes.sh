# DE Zoomcamp - Week 1 
# this script is for documentation purposes and is not meant to be run automatically





#-------------------------------------------------------------
# Code Along/Notes: 1.2.1 Intro to Docker
#-------------------------------------------------------------

# look for hello-world image in docker hub, download and run it 
docker run hello-world 

# run ubuntu image in interactive mode (-it) and parameter (bash) to run command within the image
docker run -it ubuntu bash

# run an image with specified tag (3.9) and open python 
docker run -it python:3.9

# problem: in the previous image, none of the libraries like pandas or os are available. Therefore we want to install pandas on the image, before we enter the python environment
# solution: we overwrite the python entrypoint and manually install pandas in the interactive mode

docker run -it --entrypoint=bash python:3.9
pip install pandas                                  # gets installed in the container
python                                              # opens python in the interactive mode

# problem: when we run the image again, we also need to install pandas again
# solution: build your own customized image with docker build and dockerfiles

docker build -t test:pandas .                       # image is build based on the dockerfile in the current directory
docker run -it test:pandas                          # with v0 code uncommented in dockerfile

# problem: we don't want to run our oython scripts manually in the container
# solution: now we create a python script (pipeline) which we run in the container

docker build -t test:python_pipeline .                      # image is build based on the dockerfile in the current directory
docker run -it test:python_pipeline 2022-01-17              # with v1.1 code uncommented in dockerfile and day parameter
docker run -it -e "DAY=2023-01-17" test:python_pipeline     # with v1.1 code uncommented in dockerfile and day parameter

# problem: how to load data
docker build -t pandas:test_pipeline .              # image is build based on the dockerfile in the current directory
docker run pandas:test_pipeline .                   # with v1.2 code uncommented in Dockerfile








#-------------------------------------------------------------
# Code Along/Notes: 1.2.2 Data Ingestion
#-------------------------------------------------------------


# step1: setting up a postgres in docker and a mounted folder
# --------------------------------------------------------------

# Notes: 
# - make sure to define -e variables before the image:tag command/argument
# - backslash indicates a linebreak for better readability
# -reg. mounting:
#   problem: when we save data in a database, the state is lost once the container goes offline.
#   solution: we mount a folder from the local maschine to the container so that the data is still there, independent of the container
# -reg. ports:
#   problem: docker needs the full path
#   solution: for linux systems (pwd) works (see above)
# -reg. changing the password
#   problem: when you run the docker run command and mount a folder, a database gets generated in that folder with the users and credentials you specified in the command. If you run the same command with different specifications, but do not delete the mounted folder, you will run into credential problems, because the old folder is already there and will not be overwritten
#   question: how to overwrite the mounted folder?
#   solution: TODO

# run docker container with a postgres database
docker run -it                  \   
  # set a name for the docker container
  --name postgres-db            \
  # set environmental variables
  -e POSTGRES_USER="root"       \   
  -e POSTGRES_PASSWORD="root"   \
  -e POSTGRES_DB="ny_taxi"      \
  # -v (volume) mounting: mapping a folder from the host maschine to a folder in container
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \ 
  # -p setting the ports: host-maschine:container bc I have pg installed locally, it needs to be different from 5432
  -p 5432:5432                  \  
  # specifying the image 
  postgres:13                       

# the above does not work if copy and pasted into the terminal. 
# I want to find out how to have a scripts with comments from which I can paste stuff into the terminal
docker run -it --name postgres-db -e POSTGRES_USER="root" -e POSTGRES_PASSWORD="root" -e POSTGRES_DB="ny_taxi" -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data -p 5432:5432 postgres:13

# minimal example 
# you don't necessarily need to specify a user, the default user and db name is postgres
docker run -it -e POSTGRES_PASSWORD=root -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data -p 5432:5432 postgres:13

# step2: connecting to the database
# --------------------------------------------------------------

# Notes
# now we created a pg database in the specified folder and we will try to access it via the port and the credentials we specified
# problem: how to connect to a pg database?
# solution: we can use the pgcli (postgres command line interface)

# step 2.1 open new terminal:
pip install pgcli                      # if not already installed
pgcli --help                           # open the manual
pgcli -h localhost -p 5432 -u root -d ny_taxi  # the password will be asked in an interactive prompt
\dt                                    # list all tables
\d table_name                          # describe a table

# step3: import data
# --------------------------------------------------------------

# Notes
# before we can loading data into the connected DB we need to import it. We can use python and do this within a jupyter notebook (as interactive env)
# -reg. curl: always pay attention to the URL from which you download!
#   -L flag tells curl to follow redirects, 
#   -J flag tells it to automatically set the filename based on the URL, 
#   -O flag tells it to save the file with the same name as the remote file.                       

# step 3.2 download the data & copy it into current directory
curl -o ~/Downloads/yellow_tripdata_2021-01csv.gz https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
cp ~/Downloads/yellow_tripdata_2021-01.csv .  # cp to copy a file into the current dir

# alternative: download and unzip it directly into the current directory
curl -LJO https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
gunzip ./yellow_tripdata_2021-01.csv.gz    

# alternative with wget
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz -O 'yellow_tripdata_2021-01.csv.gz'


# step4: explore dataset
# ------------------------------------------

# Notes 
# taking a first look at the dataset
less yellow_tripdata_2021-01.csv        # one line utility to look at text data

# saving a subset in a new file
head -n yellow_tripdata_2021-01.csv > yellow-head.csv

# counting the lines in a file 
wc -l yellow_tripdata_2021-01.csv       # -l flag: count lines

# step5: load dataset into DB
# ------------------------------------------

# open a jupyter notebook
jupyter notebook 

# step6: explore data
# ------------------------------------------

# look at ealiest and most recent entry and max price paid on all trips
SELECT max(tpep_pickup_datetime), min(tpep_pickup_datetime), max(total_amount) FROM yellow_taxi_data









#-------------------------------------------------------------
# Code Along/Notes: 1.2.3 Connecting pgAdmin and Postgres 
#-------------------------------------------------------------
# DE Zoomcamp - 1.2.3 Connecting pgAdmin and Postgres 
# this script is for documentation purposes and is not meant to be run automatically

# step1: running pgAdmin in Docker

# Notes 
# pgAdmin is a UI tool to interact with databases, so we don't need to do it from the command line

docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@gpadmin.org" \    # the default parameters as env vars
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \                                      # the ports 
  dpage/pgadmin4                                    # name of the pgadmin docker image on dockerhub

docker run -it -e PGADMIN_DEFAULT_EMAIL="admin@gpadmin.org" -e PGADMIN_DEFAULT_PASSWORD="root" -p 8080:80 dpage/pgadmin4 


# step2: setting up a docker network
# ------------------------------------------------

# Notes
# problem: we have pgAdmin in one container and our database in another container. But they cannot talk to one another, there is no link between them.
# solution: we set up a container network with both containers
# TODO add docker networks docs reference

docker network create pg-network

# list all networks
docker network list

# add postgres-db to network
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --name pg-database \
  --network pg-network \
  postgres:13

# check if container was added to network
docker network inspect pg-network

# add pgAdmin container to network
docker run -it \
 -e PGADMIN_DEFAULT_EMAIL="admin@pgadmin.org" \
 -e PGADMIN_DEFAULT_PASSWORD="root" \
 --name pg-admin \
  --network pg-network \
 -p 8080:80 dpage/pgadmin4 

# check if both containers are now in the network
docker network inspect pg-network

# problem: you need multipe terminals open to run all the containers in the network
# solution: docker compose --> next video











#-------------------------------------------------------------
# Code Along/Notes: 1.2.4 Dockerizing the Ingestion script
#-------------------------------------------------------------

# convert jupyter notebook to script
jupyter nbconvert --to=script exploring_122-data-ingestion_upload-data.ipynb --output="upload-data"


# testing if we successfully transformed the notebook to a script
# and if we can pass parameters to upload.data.py
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

python upload-data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db_name=ny_taxi \
    --tbl_name=yellow_taxi_data \
    --url=${URL} 

# dockerizing the pipeline
# buid the container specified in the Dockerfile
docker build -t taxi_ingest:v001 .

# parameters to docker
# parameters to the job (upload-data)

URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

docker run -it \
  --network=pg-network \
    taxi_ingest:v001 \
      --user=root \
      --password=root \
      --host=pg-database \
      --port=5432 \
      --db_name=ny_taxi \
      --tbl_name=yellow_taxi_data \
      --url=${URL}









#-------------------------------------------------------------
# Code Along/Notes: 1.2.5 Docker Compose
#-------------------------------------------------------------

# check running containers and stop them 
docker ps

# set up container as specified in docker-compose.yaml
docker-compose up

# TODO how to persist pgAdmin ?

# if you run it in detached mode (-d flag) you can shut it down with:
docker-compose down

# if its in interactuve mode (-it flag) you can run ctrl+c












#-------------------------------------------------------------
# Code Along/Notes: 1.2.6 SQL Refresher
#-------------------------------------------------------------

# check how many rows are in zones
SELECT 
  *
FROM
  zones;

# add limit to returned rows
SELECT 
  *
FROM
  yellow_taxi_data
LIMIT 100;

# now we want to do a join 

# notes
# -reg. column names: a column name needs to be in quotes it its written with capital letters

## option 1: inner join with where

```sql
SELECT 
	tpep_pickup_datetime,	
	tpep_dropoff_datetime,
	total_amount,
	-- concat adds values of multiple comluns together
	CONCAT(zones_pickup."Borough", ' / ', zones_pickup."Zone") AS "pickup_loc",
	CONCAT(zones_dropoff."Borough", ' / ', zones_dropoff."Zone") AS "dropoff_loc"
FROM
  -- use yellow_taxi_data as taxi in this query
  yellow_taxi_data taxi,
  -- this selects the zones tables once as zones_pickup 
  zones zones_pickup,
  -- and once as zones_dropoff
  zones zones_dropoff
-- this part is where the join happens, its more of a filter than a join
WHERE
  taxi."PULocationID" = zones_pickup."LocationID" AND
  taxi."DOLocationID" = zones_dropoff."LocationID"
LIMIT 100;
```

# option 1.2: inner join with join
```sql
SELECT 
	tpep_pickup_datetime,	
	tpep_dropoff_datetime,
	total_amount,
	-- concat adds values of multiple comluns together
	CONCAT(zones_pickup."Borough", ' / ', zones_pickup."Zone") AS "pickup_loc",
	CONCAT(zones_dropoff."Borough", ' / ', zones_dropoff."Zone") AS "dropoff_loc"
FROM
  yellow_taxi_data taxi JOIN zones zones_pickup
  	ON taxi."PULocationID" = zones_pickup."LocationID"
  JOIN zones zones_dropoff
  	ON "DOLocationID" = zones_dropoff."LocationID"
LIMIT 100;
```

# option 3


# question: are there empty pickup/dropoff locations

```sql
SELECT 
	tpep_pickup_datetime,	
	tpep_dropoff_datetime,
	total_amount,
	"PULocationID",
	"DOLocationID"
FROM
  yellow_taxi_data taxi 
WHERE "DOLocationID" is NULL
LIMIT 100;
```

# question: are there any ID's in Zones that are not present in the taxi tripos dataset?

```sql
SELECT 
	tpep_pickup_datetime,	
	tpep_dropoff_datetime,
	total_amount,
	"PULocationID",
	"DOLocationID"
FROM
  yellow_taxi_data taxi 
--we add a select statement after the NOT IN
WHERE "DOLocationID" NOT IN (SELECT "LocationID" FROM zones)
LIMIT 100;
```

# question: what is the day with the largest amount of trips?

```sql
SELECT 
	--DATE_TRUNC('DAY', tpep_pickup_datetime),
	CAST(lpep_pickup_datetime AS DATE) AS "day",
	COUNT(1) as "count"
FROM
  green_taxi_data taxi
--WHERE "day" = '2019-01-15'
GROUP BY 
	CAST(lpep_pickup_datetime AS DATE)
ORDER BY "count" DESC;
```

# adding some more aggregations

```sql
SELECT 
	--DATE_TRUNC('DAY', tpep_pickup_datetime),
	CAST(lpep_pickup_datetime AS DATE) AS "day",
	COUNT(1) as "count",
	MAX(total_amount),
	MAX(passenger_count)
FROM
  green_taxi_data taxi
--WHERE "day" = '2019-01-15'
GROUP BY 
	CAST(lpep_pickup_datetime AS DATE)
ORDER BY "count" DESC;
```

# group by multiple fields
#-------------------------------------------------------------
# Code Along/Notes: 1.3.1 Intro to Terrafrom Concepts and GCP Pre-Requisites
#-------------------------------------------------------------

# step1: install terraform

brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# step2: install GCP SDK

    # check if its installed
    gcloud -v

    # possibly install sdk form https://cloud.google.com/sdk/docs/install

    # install components with
    gcloud components install COMPONENT_ID
    # remove components with
    gcloud components remove COMPONENT_ID

    # initialize GC CLI with 
    gcloud init

# step3: authenticate GCP project with local maschine via SDK

    # OAuth Way
    # export authentication token that was downloaded in the set-up of a project 
    export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"

    # Refresh token/session, and verify authentication
    gcloud auth application-default login

    # follow the re-directs and your local setup is authenticated with the cloud anvironment
    # more info on web tokens: https://jwt.io/introduction/










#---------------------------------------------------------------------
# Code Along/Notes: 1.4.1 Setting up the Environment on Google Cloud
#---------------------------------------------------------------------

# connect to machine via ssh
ssh -i ~/.ssh/id_gcp lisa@34.155.54.252
# or 
ssh de-zoomcamp

# check out the machine
htop

# gcloud cli is already installed on the vm, we can check with 
gcloud --version

# configuring the vm instance

# step1: install anaconda
wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh

# step2: install docker
    # get list of packages
    sudo apt-get update
    # install docker
    sudo apt-get install docker.io

    # try running it
    docker run hello-world          # doesn't work bc of missing permissions
    # give it permissions 
    # see https://github.com/sindresorhus/guides/blob/main/docker-without-sudo.md
    sudo groupadd docker    # might already exist 
    # add user 
    sudo gpasswd -a $USER docker    # this way you don't need to use sudo all the time
    # restart service
    sudo service docker restart 

# step3: configure VSCode to work on machine 
    # go to extentions and install remote - SSH / add SSH Host via prompt

# step4: install docker compose
    # create folder for executable files bin
    mkdir bin

    # download the docker-compose release https://github.com/docker/compose/releases/download/v2.15.1/docker-compose-linux-x86_64
    wget https://github.com/docker/compose/releases/download/v2.15.1/docker-compose-linux-x86_64 -O docker-compose

    # tell the system that this is an executable file
    chmod +x docker-compose

    # since we don't want to do this everytime from the bin directory we need to add it to the PATH Variable. This way it gets visible from every directory
    cd .
    nano .bashrc
    # add this to the end
    PATH="${HOME}/bin:${PATH}"   # before the colon is what we want to prepend, after the colon is the former PATH
    # press ctrl+o to save it and enter to overwrite file 
    # press ctrl+x to exit nano

    # source bashrc to enable changed
    source .bashrc

# step 5: run docker-compose
    # go to week1/sql
    docker-compose up -d

    # check it its running 
    docker ps

# step6: install pgcli
    cd 
    pip install pgcli
    # connect to postgres
    pgcli -h localhost -U root -d ny_taxi

    # alternative way 
    conda install -c conda-forge pgcli   # installs compiled version
    # update pip list
    pip install -U mycli

# step7: how to forward the port from VM localhost to our local machine
    # in the SSH VSCode Window go to Ports Tab and click on forward port
    # then connect to it from local VSCode
    pgcli -h localhost -U root -d ny_taxi

# step8: install terraform
    # go to https://developer.hashicorp.com/terraform/downloads
    # copy the link to the binary amd64
    # cd into bin directory and
    wget https://releases.hashicorp.com/terraform/1.3.7/terraform_1.3.7_linux_amd64.zip
    # unzip it with
    sudo apt-get install unzip
    unzip terraform_1.3.7_linux_amd64.zip
    # remove zip file
    rm terraform_1.3.7_linux_amd64.zip
    # check if its already executable

    # setup the service worker credentials
    # for this the JSON file needs to land on the google VM, we can use ftp transfer
    sftp de-zoomcamp
    put dtc-de-375708-9120d1930b33.json

    # now we need to connect it to the cloud but we cannot use the OAuth method 
    # instead we use the key file
    # again we export the ENV Variable
    export GOOGLE_APPLICATION_CREDENTIALS="~/.gc/dtc-de-375708-9120d1930b33.json"

    # now we use this file with 
  

        #debugging
        echo $GOOGLE_APPLICATION_CREDENTIALS

    # step8: stopping the VM on GCP
    sudo shutdown now
