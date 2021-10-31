# awsChallenge
Create a template to deploy with CloudFormation for a Serverless Application with API Gateway, Lambda, S3 and CloudWatch.

### Commands
	- sam init --runtime python3.9 --name pytask
	- sam build
	- sam deploy --guided --capabilities CAPABILITY_IAM
	- Deploy
		- aws cloudformation deploy --stack-name task --template-file template.yaml --capabilities CAPABILITY_NAMED_IAM
	- Lambda Code
		- aws lambda update-function-code --function-name  task-lambda-function --zip-file fileb://Code.zip
		- aws s3api put-object --bucket text-content --key Code.zip --body Code.zip

### TODO
	- Logger in a separate module

### Testing cases
	- Verify transformation fails
	- Verify JSON parse fails as expected (Error response code)
	- Verify external functions are called with appropriate parameters
