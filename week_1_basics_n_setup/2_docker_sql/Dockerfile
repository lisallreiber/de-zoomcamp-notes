# # v0: basic version
# # -----------------------------------------------
# # specify image
# FROM python:3.9.1

# # bash code
# RUN pip install pandas

# ENTRYPOINT [ "bash" ]


#  v1.1: simple version
# -----------------------------------------------
# FROM python:3.9.1

# RUN pip install pandas 

# WORKDIR /app
# COPY pipeline.py pipeline.py
# ENV DAY="today"

# # here we define what docker is supposed to run in the container
# ENTRYPOINT [ "python", "pipeline.py" ]

# #  v1.2: final version
# # -----------------------------------------------
# FROM python:3.9.1

# RUN apt-get install wget
# RUN pip install pandas sqlalchemy psycopg2

# WORKDIR /app
# COPY ingest-data.py ingest-data.py 

# ENTRYPOINT [ "python", "ingest-data.py" ]

#  v1.2: homework version
# -----------------------------------------------
FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY ingest-data-green.py ingest-data-green.py 

ENTRYPOINT [ "python", "ingest-data-green.py" ]