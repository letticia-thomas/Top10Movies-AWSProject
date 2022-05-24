import boto3
import json
import locale

def lambda_handler(event, context):
	s3_client = boto3.client("s3")
	S3_BUCKET = 'letticiaawsbucket'
	sqs = boto3.client('sqs',endpoint_url = 'https://sqs.eu-central-1.amazonaws.com')
	queue_url = 'https://sqs.eu-central-1.amazonaws.com/911776993970/topMovieQueue'
	object_key = "Top250Movies.json"
	file_content = s3_client.get_object(
		Bucket=S3_BUCKET, Key=object_key)
	json_data = json.loads(file_content["Body"].read().decode("utf-8"))
	items = json_data['items']
	items.sort(key=lambda x: int(locale.atof(x['imDbRating'])))
	sorted_ids=''
	for x in range(10):
		sorted_ids += items[x]["id"]
		sorted_ids = sorted_ids + '-'
	response = sqs.send_message(
		QueueUrl=queue_url,
		DelaySeconds=10,
		MessageAttributes={
        	'movies': {
            	'DataType': 'String',
            	'StringValue': sorted_ids
        	}
        },
		MessageBody= ('Message send successfully')
		)
	print(sorted_ids)
	print('sending message successfully')
