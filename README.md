# UBER-VS-LYFT
Surge analysis

#Kinesis

1. Setup Kinesis firehose on aws

2. Specify the bucket names that you want to direct the firehose to

2. Use the cronjob to run uber_lyft_api_call.py every 2 minutes


#Spark

1. Read raw data from s3

2. Create Spark dataFrames in 3 nf

3. Store them in s3 as parquet for backup

#PostgreSQL

1. Create 2 tables : Uber and Lyft

2. Read data into each table from the spark script

#Webapp

Run Spyre on a new EC2 instance, Use the final_spyre.py.

#


<img src="images/DAG.png">


<img src="images/demo.png">


<img src="images/table_on_web.png">
