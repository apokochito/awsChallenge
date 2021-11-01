import boto3

s3 = boto3.resource('s3')

def update_file(result, file_name):
	# Upload XML file to S3
    boto3.client('s3').put_object(Bucket='sam-demo-cloudformation-1', Body=result, Key=str(file_name))
    