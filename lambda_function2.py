import json
import boto3
import urllib3

s3_client = boto3.client('s3')
sqs = boto3.client('sqs',endpoint_url = 'https://sqs.eu-central-1.amazonaws.com')

def lambda_handler(event, context):
	records = event['Records']
	message = records[0]
	messageAtt = message['messageAttributes']
	movies = messageAtt['movies']
	movieIds = movies['stringValue']
	li = list(movieIds.split("-"))
	print(li)
	http = urllib3.PoolManager()
	data1 =[]
	for x in li:
		if (x != ''):
			api_url = "http://www.omdbapi.com/?i="+x+"&apikey=d5b71946"
			r = http.request('GET', api_url)
			res = r.data.decode("utf-8")
			res1 = json.loads(res)
			data1.append(res1)
	json_dump = {'items' : data1}
	resultFile = json.dumps(json_dump)
	s3_bucket = 'resultmoviebucket'
	s3_client.put_object(Bucket = s3_bucket, Key = 'sample.json', Body = resultFile)
	print('file updated')