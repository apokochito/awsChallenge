import boto3

def upload_file(result):
	# Upload XML file to S3
    boto3.client('s3').put_object(Bucket='sam-demo-cloudformation-1', Body=result, Key='new_file.xml')
    