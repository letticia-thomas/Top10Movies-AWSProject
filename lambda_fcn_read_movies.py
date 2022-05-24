import boto3
import json
import locale

# creating boto3 client for accessing s3 bucket
s3_client = boto3.client("s3")
# creating boto3 client for accessing SQS
sqs = boto3.client('sqs',endpoint_url = 'https://sqs.eu-central-1.amazonaws.com')

# SQS queue 'topMovieQueue' for sending message
queue_url = 'https://sqs.eu-central-1.amazonaws.com/911776993970/topMovieQueue'

def read_s3_bucket(s3_bucket, object_key):
	# Reading json file from s3 bucket
	file_content = s3_client.get_object(
		Bucket=s3_bucket, Key=object_key)
	
	# converting JSON string to python dictionary
	movie_dictionary = json.loads(file_content["Body"].read().decode("utf-8"))
	return(movie_dictionary['items'])

def get_top10_movieids_in_string(movie_list):
	# select top 10 movies and appending ids to string

	sorted_ids=''
	for x in range(10):
		sorted_ids += movie_list[x]["id"]
		sorted_ids = sorted_ids + '-'
	return(sorted_ids)

def send_message_SQS(top10_movie_ids):
	# sending message to SQS using sorted id as attribute
	response = sqs.send_message(
		QueueUrl=queue_url,
		DelaySeconds=10,
		MessageAttributes={
        	'movies': {
            	'DataType': 'String',
            	'StringValue': top10_movie_ids
        	}
        },
		MessageBody= ('Sending Message')
		)

def lambda_handler(event, context):

	s3_bucket = 'letticiaawsbucket'
	object_key = "Top250Movies.json"
	movie_list = read_s3_bucket(s3_bucket, object_key)

	# sorting list of movies using imDb rating
	movie_list.sort(key=lambda x: int(locale.atof(x['imDbRating'])))

	top10_movie_ids = get_top10_movieids_in_string(movie_list)
	
	send_message_SQS(top10_movie_ids)

	print('Message send successfully')
