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
	message = records[0]
	messageAtt = message['messageAttributes']
	movies = messageAtt['movies']
	movieIds = movies['stringValue']
    # fetching movie id from Message arguments
	movieIdList = list(movieIds.split("-"))

    # getting more information using imDb API
	http = urllib3.PoolManager()
	topMovieList =[]
	for movie_id in movieIdList:
		if (movie_id != ''):
			api_url = "http://www.omdbapi.com/?i="+movie_id+"&apikey=d5b71946"
			r = http.request('GET', api_url)
			response = r.data.decode("utf-8")
			responseLoad = json.loads(response)
			topMovieList.append(responseLoad)
	topMovieDictionary = {'items' : topMovieList}
	resultFile = json.dumps(topMovieDictionary)

    # S3 bucket for storing result file
	s3_bucket = 'resultmoviebucket'
	s3_client.put_object(Bucket = s3_bucket, Key = 'Sample.json', Body = resultFile)
	print('file updated 1')