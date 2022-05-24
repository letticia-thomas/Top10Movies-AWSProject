import boto3
import json
import locale

# creating boto3 client for accessing s3 bucket
s3_client = boto3.client("s3")
# creating boto3 client for accessing SQS
sqs = boto3.client('sqs',endpoint_url = 'https://sqs.eu-central-1.amazonaws.com')

# json file consisting of top 250 movies stored in this bucket
S3_BUCKET = 'letticiaawsbucket'
object_key = "Top250Movies.json"
# SQS queue 'topMovieQueue' for sending message
queue_url = 'https://sqs.eu-central-1.amazonaws.com/911776993970/topMovieQueue'

def lambda_handler(event, context):
	
	# Reading json file from s3 bucket
	file_content = s3_client.get_object(
		Bucket=S3_BUCKET, Key=object_key)
	
	# converting JSON string to python dictionary
	movie_dictionary = json.loads(file_content["Body"].read().decode("utf-8"))
	movie_list = movie_dictionary['items']

	# sorting list of movies using imDb rating
	movie_list.sort(key=lambda x: int(locale.atof(x['imDbRating'])))

	# sorted ids appending to string
	sorted_ids=''
	for x in range(10):
		sorted_ids += movie_list[x]["id"]
		sorted_ids = sorted_ids + '-'
	
	# sending message to SQS using sorted id as attribute
	response = sqs.send_message(
		QueueUrl=queue_url,
		DelaySeconds=10,
		MessageAttributes={
        	'movies': {
            	'DataType': 'String',
            	'StringValue': sorted_ids
        	}
        },
		MessageBody= ('Sending Message')
		)
	print('Message send successfully')
