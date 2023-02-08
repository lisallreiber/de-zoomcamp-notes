## Week 2 Homework: Workflow Orchestration <!-- omit from toc -->

- [Question 1. Load January 2020 data](#question-1-load-january-2020-data)
- [Question 2. Scheduling with Cron](#question-2-scheduling-with-cron)
- [Question 3. Loading data to BigQuery](#question-3-loading-data-to-bigquery)
- [Question 4. Github Storage Block](#question-4-github-storage-block)
- [Question 5. Email notifications](#question-5-email-notifications)
- [Question 6. Secrets](#question-6-secrets)
- [Submitting the solutions](#submitting-the-solutions)
- [Learning in public](#learning-in-public)

The goal of this homework is to familiarise users with workflow orchestration. 

## Question 1. Load January 2020 data

Using the `etl_web_to_gcs.py` flow that loads taxi data into GCS as a guide, create a flow that loads the green taxi CSV dataset for January 2020 into GCS and run it. Look at the logs to find out how many rows the dataset has.

How many rows does that dataset have?

* **447,770 ✅**
* ~~766,792~~
* ~~299,234~~
* ~~822,132~~

**steps:**

```bash
# cd to top-level folder
cd week_2_workflow_orchestration
# activate conda environment
conda activate de-zoomcamp
```
- adapt the [etl_web_to_gcs.py flow](02_gcp/etl_web_to_gcs.py) to load the green taxi data for January 2020
- run the flow from [new etl script](04_homework/etl_web_to_gcs.py)

```bash
# start prefect
prefect orion start 
# run the flow  
python flows/04_homework/etl_web_to_gcs.py
```

- go to prefect orion dashboard at http://127.0.0.1:4200
- navigate to the flow and check the logs for the printed output of `print(f"rows: {len(df)}")`

**✅ Answer: 447,770**

## Question 2. Scheduling with Cron

Cron is a common scheduling specification for workflows. 

Using the flow in `etl_web_to_gcs.py`, create a deployment to run on the first of every month at 5pm UTC. What’s the cron schedule for that?

- **`0 5 1 * *` ✅**
- ~~`0 0 5 1 *`~~
- ~~`5 * 1 0 *`~~
- ~~`* * 5 1 0`~~

**steps**

- via prefect CLI: build and apply a deployment to prefect cloud and specify the cron schedule
- using https://crontab.guru/ to define CRON schedule
- -a flag also applies the deployment
- -t flag adds a tag to the deployment
```bash
prefect deployment build flows/04_homework/parameterized_flow.py:etl_parent_flow -n "Paramerized ETL from CLI" --cron "0 5 1 * *" -a -t homework
```

**✅ Answer: 0 5 1 \* \***

## Question 3. Loading data to BigQuery 

Using `etl_gcs_to_bq.py` as a starting point, modify the script for extracting data from GCS and loading it into BigQuery. This new script should not fill or remove rows with missing values. (The script is really just doing the E and L parts of ETL).

The main flow should print the total number of rows processed by the script. Set the flow decorator to log the print statement.

Parametrize the entrypoint flow to accept a list of months, a year, and a taxi color. 

Make any other necessary changes to the code for it to function as required.

Create a deployment for this flow to run in a local subprocess with local flow code storage (the defaults).

Make sure you have the parquet data files for Yellow taxi data for Feb. 2019 and March 2019 loaded in GCS. Run your deployment to append this data to your BiqQuery table. How many rows did your flow code process?

- **14,851,920 ✅**
- ~~12,282,990~~
- ~~27,235,753~~
- ~~11,338,483~~

**steps**
- use the [parameterized ETL Flow](03_deployment/parameterized_flow.py) to load the yellow taxi data for February 2019 and March 2019 into GCS
  - set the months parameter to `months=[2,3]`
  - set year to `2019`
  - set color to `yellow`
  
- [adapt the etl_gcs_to_bq.py flow](04_homework/etl_gcs_to_bq.py) to load the yellow taxi data for February 2019 and March 2019
    - add flow factory for Feb and Mar Flows
    - keep track of processed rows with print statement
    - build & apply deployment and run it
```bash
## build and apply deployment
prefect deployment build flows/04_homework/etl_gcs_to_bq.py:etl_factory_flow -n "ETL GCS to BQ" --flow-storage-type local -a -t homework

## run deployment
prefect deployment run "etl-factory/ETL GCS to BQ"
```

**✅ Answer: 14,851,920**

## Question 4. Github Storage Block

Using the `web_to_gcs` script from the videos as a guide, you want to store your flow code in a GitHub repository for collaboration with your team. Prefect can look in the GitHub repo to find your flow code and read it. Create a GitHub storage block from the UI or in Python code and use that in your Deployment instead of storing your flow code locally or baking your flow code into a Docker image. 

Note that you will have to push your code to GitHub, Prefect will not push it for you.

Run your deployment in a local subprocess (the default if you don’t specify an infrastructure). Use the Green taxi data for the month of November 2020.

How many rows were processed by the script?

- ~~88,019~~
- ~~192,297~~
- **88,605 ✅**
- ~~190,225~~

**steps**
- create a github storage block in the UI
     ```bash
    pip install prefect-github            
    prefect block register -m prefect_github  

    # or generate one with code
    python blocks/make_github_block.py 
    ```
- create a [github_deploy.py](04_homework/github_deploy.py) script to build and apply the deployment from Github code
    ```bash
    python flows/04_homework/github_deploy.py     
    ```
- OR build deployment via CLI
    <!-- ```bash
    prefect deployment build flows/04_homework/etl_web_to_gcs.py:etl_web_to_gcs --name github_deploy --tag dev -sb github/test-gh
    ``` -->

    ```bash
    prefect deployment build ./week_2_workflow_orchestration/flows/04_homework/etl_web_to_gcs.py:etl_web_to_gcs -n etl-from-github -sb github/de-zoomcamp-github/ --params='{"year":2020, "month":11, "color":"green"}' --tag homework --apply
    ```
- get the number of processed rows from the prefect logs 

<!-- open question: where is the locally written data and how do I specify the path to it? -->

**✅ Answer: 88,605**

## Question 5. Email notifications

The hosted Prefect Cloud lets you avoid running your own server and has automations that allow you to get notifications when certain events occur or don’t occur. 

Create a free forever Prefect Cloud account at [app.prefect.cloud](https://app.prefect.cloud/) and connect your workspace to it following the steps in the UI when you sign up. 

Set up an Automation that will send yourself an email when a flow run succeeds. Run the deployment used in Q4 for the Green taxi data for April 2019. Check your email to see a success notification.

How many rows were processed by the script?

- ~~`125,268`~~
- ~~`377,922`~~
- ~~`728,390`~~
- **`514,392` ✅**

**steps**

- create a free account at [app.prefect.cloud](https://app.prefect.cloud/)
- login with API token
    ```bash
    prefect login cloud
    ```
- create a new profile
    ```bash
    prefect profile create prefect-cloud
    ```
- run [make_github_blcok.py script](../blocks/make_github_block.py) to create github block in the cloud  
    ```bash
    python blocks/make_github_block.py
    ```
- run the [github_deploy.py](04_homework/github_deploy.py) script to build and apply the deployment from Github code
    ```bash
    python flows/04_homework/github_deploy.py     
    ```
- run the deployment with new parameters
    ```bash
    prefect deployment run "etl-web-to-gcs/github-flow" --params='{"year":2019, "month":4, "color":"green"}' --tag homework 
    ```
- start an agent
    ```bash
    prefect agent start --work-queue "default"
    ```
- read the number of rows from the logs
  
**Answer: 514,392 ✅**

## Question 6. Secrets

Prefect Secret blocks provide secure, encrypted storage in the database and obfuscation in the UI. Create a secret block in the UI that stores a fake 10-digit password to connect to a third-party service. Once you’ve created your block in the UI, how many characters are shown as asterisks on the next page of the UI (*).

- ~~5~~
- ~~6~~
- **8 ✅**
- ~~10~~

**steps**
- add a secret block in the Prefect Cloud UI and enter a 10-digit secret
- check how many (*) are shown

**Answer: 8 ✅**

## Submitting the solutions

* Form for submitting: 
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 6 February (Monday), 22:00 CET

## Learning in public

- [Prefect Cloud Interface Tweet](https://twitter.com/lisa_reiber/status/1623375846303010824?s=20&t=l3B3Fs-UygcQLsg--63YnQ)
- [Tech Setup Tweet](https://twitter.com/lisa_reiber/status/1622518653274009600?s=20&t=l3B3Fs-UygcQLsg--63YnQ)
- [Working in public: timeout argument is your friend tweet](https://twitter.com/lisa_reiber/status/1622926816246898688?s=20&t=l3B3Fs-UygcQLsg--63YnQ)
- [Coding with Github Copilot: standard syntax](https://twitter.com/lisa_reiber/status/1621529827416375296?s=20&t=l3B3Fs-UygcQLsg--63YnQ)
- [Coding with Github Copilot: forloops](https://twitter.com/lisa_reiber/status/1621557985423015938?s=20&t=l3B3Fs-UygcQLsg--63YnQ)