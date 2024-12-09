# Twitch Clip Ingestion Service

## About
This project sets up a Lambda function whose responsibility is to fetch clips from a given broadcaster from Twitch and
stores the clip metadata in DynamoDB for future processing. This project is purely for learning purposes in order to familarize
myself with AWS services and their integrations.

## Local Development

### Pre-requisites
- Install AWS CLI
- Install SAM CLI
- Install & run Docker
- Have your Twitch app's `client-id` and `client-secret` ready

### Dependencies
Use `pipenv install --dev` to install all packages
and to set up the dev environment

### Locally Invoking the Lambda
You will need to do two things:
1. Spin up a local DynamoDB instance
2. Use SAM to invoke the Lambda function

#### Setting up the DynamoDB Instance
1. Set up a local AWS profile using `aws configure --profile local`. Make note of all the values you pass in for each option.
They can be dummy values.
2. Use the provided `compose.yml` file to build and start the container
with `docker compose up`
3. Create the table with the provided table in `dynamo/users-definition.json` with this command
`aws dynamodb create-table --cli-input-json file://dynamo/users-definition.json --endpoint-url http://localhost:8000 --profile local`
4. (Optional) To view any changes on the table invoke `aws dynamodb scan --table-name users --endpoint-url http://localhost:8000 --profile local`

#### Building the Lambda Function
1. Run `pipenv requirements > requirements.txt`. This
is because SAM looks for a `requirements.txt` to build the project with pip. You will only need to run this again if you change dependencies.
2. Update `template.yaml` to pass in the values of `CLIENT_ID`,`CLIENT_SECRET`, `AWS_ACCESS_ID`, `AWS_ACCESS_KEY`, and `AWS_REGION`.
3. Invoke `sam build`

### Invoking the Lambda Function
Use `sam local invoke --event events/<name_of_event>.json` to invoke the Lambda function

For example, passing in the `get_health.json` file to the above command produces the following response:

```json
 {"statusCode": 200, "body": "{\"message\":\"Looks like things are up and running!\"}", "isBase64Encoded": false, "headers": {"Content-Type": "application/json"}}
```
