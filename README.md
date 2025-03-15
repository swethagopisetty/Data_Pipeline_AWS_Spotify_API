# Spotfiy Data Pipeline End-To-End Data Engineering Project

### Introduction
In this project we build an ETL pipeline using Spotify API on AWS. The pipeline will retrieve the data from Spotify API, transform it to a desired  format and load it into an AWS data store.

### Architecture
![Architecture Diagram](https://github.com/swethagopisetty/spotify-end-to-end-data-engineering-project/blob/main/Spotify_Data_Pipeline.jpg)


### About Dataset/API
This API contains information about music artist, albums and songs that reached Global Charts in [Spotify API](https://developer.spotify.com/documentation/web-api)

### Services Used

1. **S3(Simple Storage Service):** Amazon S3 (Simple Storage Service) is a highly scalable object storage service that can store and retrieve any amount of data from anywhere on the web. It is commonly used to store and distribute large media files, data backups, and static website files. 

2. **AWS Lambda:** AWS Lambda is a serverless computing service that lets you run your code without managing servers. You can use Lambda to run code in response to events like changes in S3, DynamoDB, or other AWS services.

3. **Cloud Watch:** Amazon CloudWatch is a monitoring service for AWS resources and the applications you run on them. You can use CloudWatch to collect and track metrics, collect and monitor log files and set alarms.

4. **Glue Crawler:** AWS Glue Crawler is a fully managed service that automatically crawls your data sources, identifies data formats and infers schemas to create an AWS GLue Catalog.

5. **Data Catalog:** AWS Glue Data Catalog is a fully managed metadata repository that makes it easy to discover and manage data in AWS. You can use the Glue Data Catalog with other AWS services, such as Athena.

6. **Amazon Athena:** Amazon Athena is an interactive query service that makes it easy to analyze data in Amazon S3 using standard SQL. You can use Athena to analyze data in your Glue Data Catalog or in other S3 buckets.

### Install Packages
```
pip install pandas
pip install numpy
pip install spotify
```

### Project Execution Flow
Extract Data from API -> Lambda Trigger (every 1 hour) -> Run Extract Code -> Store Raw data -> Trigger Transform Function -> Transform Data and Loat It -> Query Using Athena
