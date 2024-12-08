# Twitch Clip Ingestion Service

## About
This project sets up a Lambda function whose responsibility is to fetch clips from a given broadcaster from Twitch and
stores the clip metadata in DynamoDB for future processing. This project is purely for learning purposes in order to familarize
myself with AWS services and their integrations.

## Local Development

### Dependencies
Use `pipenv install --dev` to install all packages
and to set up the dev environment

### Locally Invoking the Lambda
You will need to do two things:
1. Spin up a local DynamoDB instance
2. Use SAM to invoke the Lambda function

#### Setting up the DynamoDB Instance


#### Building the Lambda Function
Before you build the local Lambda, first do the following:
- Install SAM CLI
- Have Docker running in the background

1. Run `pipenv requirements > requirements.txt`. This
is because SAM looks for a `requirements.txt` to build the project with pip. You will only need to run this again if you change dependencies.
2. Invoke `sam build`

### Invoking the Lambda Function
Use `sam local invoke --event events/<name_of_event>.json` to invoke the Lambda function

For example, passing in the `get_health.json` file to the above command produces the following response:

```json
 {"statusCode": 200, "body": "{\"message\":\"Looks like things are up and running!\"}", "isBase64Encoded": false, "headers": {"Content-Type": "application/json"}}
```
