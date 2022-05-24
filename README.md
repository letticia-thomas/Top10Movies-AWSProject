# Top 10 IMDB rated movies

This project list the top 10 IMDB rated movies from a list of movies using aws services.

## Description

The aim of this project is to list the top 10 IMDB rated movies from a list and enrich this list with more information about the movie. We use aws services to do this project.

* Complete list of movies are stored in an aws S3 bucket in the JSON format
* Use aws Lamda function(serverless function) to read the JSON file.
* Read the JSON file, we sort the list and find top 10 IMDB rated movies.
* Then we send a messege to the aws SQS queue with movie id information
* Once a message is in the SQS queue, it will trigger another lambda function which helps to continue the workflow
* In the lamda function we get the filtered movie ids from the sqs event and prepare the final list to store/display
* Using IMDB API, with the help of movie ids, get more information and enrich the movie list
* Create a JSON file with movie list and store it in another S3 bucket
## Getting Started

### Dependencies
* boto3

### How to run
* Trigger the lambda function which read from s3 bucket. Thats it, find the result in S3 bucket
