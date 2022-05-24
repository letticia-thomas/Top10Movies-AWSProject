import json
import boto3
import urllib3

# creating boto3 client for accessing s3 bucket
s3_client = boto3.client('s3')
# creating boto3 client for accessing SQS
sqs = boto3.client('sqs',endpoint_url = 'https://sqs.eu-central-1.amazonaws.com')

# This lambda function will get triggered when message is updated in SQS queue

def lambda_handler(event, context):
   
    # retrieving message from event
	records = event['Records']
	message_info = records[0]
	message_attribute = message_info['messageAttributes']
	movies = message_attribute['movies']
	movie_ids = movies['stringValue']

    # fetching movie id from Message arguments
	movie_id_list = list(movie_ids.split("-"))

    # getting more information using imDb API
	http = urllib3.PoolManager()
	top_movie_list =[]
	for movie_id in movie_id_list:
		if (movie_id != ''):
			api_url = "http://www.omdbapi.com/?i="+movie_id+"&apikey=d5b71946"
			r = http.request('GET', api_url)
			response = r.data.decode("utf-8")
			response_load = json.loads(response)
			top_movie_list.append(response_load)
	top_movie_dictionary = {'items' : top_movie_list}
	result_file = json.dumps(top_movie_dictionary)

    # S3 bucket for storing result file
	s3_bucket = 'resultmoviebucket'
	s3_client.put_object(Bucket = s3_bucket, Key = 'Top10Movies.json', Body = result_file)
	print('file updated')