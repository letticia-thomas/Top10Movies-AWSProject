import json
import boto3
import urllib3

def get_more_imdb_info(imdb_id):
	# getting more information using imDb API

	http = urllib3.PoolManager()
	api_url = "http://www.omdbapi.com/?i="+imdb_id+"&apikey=d5b71946"
	try:
		response_raw = http.request('GET', api_url)
		response_formatted = response_raw.data.decode("utf-8")
		return(response_formatted)
	except:
  		print("API is not returning any data") 

def get_movie_ids_from_SQS_event(event):
	# retrieving message from event

	records = event['Records']
	message_info = records[0]
	message_attribute = message_info['messageAttributes']
	movies = message_attribute['movies']

	# return movie id from Message attribute
	movie_ids = movies['stringValue']
	return(list(movie_ids.split("-")))

def enrich_movie_list(movie_id_list):
	# create list of top 10 movies with enriched data

	top_movie_list = []
	for movie_id in movie_id_list:
		if (movie_id != ''):
			response = get_more_imdb_info(movie_id)
			response_load = json.loads(response)
			top_movie_list.append(response_load)
	return({'items' : top_movie_list})

def store_data_in_S3_bucket(enriched_data):
	# Stores JSON file in S3 bucket

	# creating boto3 client for accessing s3 bucket
	s3_client = boto3.client('s3')
	# S3 bucket for storing result file
	s3_bucket = 'resultmoviebucket'
	s3_client.put_object(Bucket = s3_bucket, Key = 'Top10Movies.json', Body = json.dumps(enriched_data))

# This lambda function will get triggered when message is updated in SQS queue

def lambda_handler(event, context):
	movie_id_list = get_movie_ids_from_SQS_event(event)
	enriched_data = enrich_movie_list(movie_id_list)
	store_data_in_S3_bucket(enriched_data)
	print('file updated')