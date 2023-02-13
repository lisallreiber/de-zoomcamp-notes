Week 3: Data Warehouses <!-- omit from toc -->
------------------------------

- [3.1.1 Data Warehouse and BigQuery](#311-data-warehouse-and-bigquery)
  - [OLAP vs OLTP](#olap-vs-oltp)
  - [Data Warehouse](#data-warehouse)
  - [Partitoning and clustering](#partitoning-and-clustering)
  - [Best practices](#best-practices)
  - [Internals of BigQuery](#internals-of-bigquery)
  - [Advanced](#advanced)
    - [ML](#ml)
      - [Deploying ML model](#deploying-ml-model)
  - [Homework](#homework)
- [Community notes](#community-notes)


## 3.1.1 Data Warehouse and BigQuery

- [Slides](https://docs.google.com/presentation/d/1a3ZoBAXFk8-EhUsd7rAZd-5p_HpltkzSeujjRGB2TAI/edit?usp=sharing)  
- [Big Query basic SQL](big_query.sql)

### OLAP vs OLTP

- OLTP: Online Transaction Processing
- OLAP: Online Analytical Processing

Here's a table comparing OLTP and OLAP data warehouses based on different characteristics:

| Characteristics    | OLTP                                                                | OLAP                                                           |
| :----------------- | :------------------------------------------------------------------ | :------------------------------------------------------------- |
| Purpose            | Transactions Processing                                             | Data Analysis and Business Intelligence                        |
| Data Updates       | Frequent and Small                                                  | Infrequent and Large                                           |
| Database Design    | Normalized                                                          | Denormalized or Star Schema                                    |
| Space Requirements | Relatively Small                                                    | Large                                                          |
| Query Performance  | Fast for small, simple queries                                      | Slower for complex queries, but optimized for analysis         |
| Data Integrity     | High data integrity maintained through transactions and constraints | Data may be slightly stale, but consistency is not as critical |
| Data Scope         | Limited, typically only current data                                | Historical data, often including aggregations                  |


OLTP (Online Transaction Processing) data warehouses are optimized for fast transactions processing, such as inserting, updating, and retrieving small amounts of data. They are designed with a high level of data normalization to maintain data integrity, but this also results in complex relationships and slow query performance.

OLAP (Online Analytical Processing) data warehouses, on the other hand, are optimized for data analysis and business intelligence. They use a denormalized or star schema design, which enables faster query performance at the cost of some data redundancy. OLAP systems are typically larger and store more historical data, including aggregated data, which is used for analysis.



### Data Warehouse

- [Data Warehouse and BigQuery](https://youtu.be/jrHljAoD6nM)

### Partitoning and clustering

- [Partioning and Clustering](https://youtu.be/jrHljAoD6nM?t=726)  
- [Partioning vs Clustering](https://youtu.be/-CqXf7vhhDs)  

### Best practices

- [BigQuery Best Practices](https://youtu.be/k81mLJVX08w)  

### Internals of BigQuery

- [Internals of Big Query](https://youtu.be/eduHi1inM4s)  

### Advanced

#### ML
[BigQuery Machine Learning](https://youtu.be/B-WtpB0PuG4)  
[SQL for ML in BigQuery](big_query_ml.sql)

**Important links**
- [BigQuery ML Tutorials](https://cloud.google.com/bigquery-ml/docs/tutorials)
- [BigQuery ML Reference Parameter](https://cloud.google.com/bigquery-ml/docs/analytics-reference-patterns)
- [Hyper Parameter tuning](https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-create-glm)
- [Feature preprocessing](https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-preprocess-overview)

##### Deploying ML model

- [BigQuery Machine Learning Deployment](https://youtu.be/BjARzEWaznU)  
- [Steps to extract and deploy model with docker](extract_model.md)  



### Homework


## Community notes

Did you take notes? You can share them here.

* [Notes by Alvaro Navas](https://github.com/ziritrion/dataeng-zoomcamp/blob/main/notes/3_data_warehouse.md)
* [Isaac Kargar's blog post](https://kargarisaac.github.io/blog/data%20engineering/jupyter/2022/01/30/data-engineering-w3.html)
* [Marcos Torregrosa's blog post](https://www.n4gash.com/2023/data-engineering-zoomcamp-semana-3/) 
* [Notes by Victor Padilha](https://github.com/padilha/de-zoomcamp/tree/master/week3)
* Add your notes here (above this line)
