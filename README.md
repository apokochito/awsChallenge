# awsChallenge
Create a template to deploy with CloudFormation for a Serverless Application with API Gateway, Lambda, S3 and CloudWatch.

### Commands
	- Deploy
		- aws cloudformation deploy --stack-name task --template-file template.yaml --capabilities CAPABILITY_NAMED_IAM
	- Lambda Code
		- aws lambda update-function-code --function-name  task-lambda-function --zip-file fileb://Code.zip