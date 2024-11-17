import os

import boto3
from aws_lambda_powertools.event_handler import ALBResolver, Response
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

from aws_lambda_powertools import Logger
from lambda_dynamo_refapp.services.clips_service import ClipsService
from lambda_dynamo_refapp.services.twitch_service import TwitchService

logger = Logger()
app = ALBResolver(enable_validation=True)

# Load Env
client_id = os.getenv("CLIENT_ID", "")
client_secret = os.getenv("CLIENT_SECRET", "")

# Setup Dynamo
dynamodb = boto3.resource("dynamodb")
users_table = dynamodb.Table("clips")
clips_table = dynamodb.Table("clips")

# Load Services
twitch_service = TwitchService(client_id, client_secret)
clips_service = ClipsService(users_table)


@app.post("/user")
def post_user(user: str) -> Response[dict]:
    clips = twitch_service.get_clips_from_broadcaster(user)
    clips_service.put_clips(user, clips)
    return Response(status_code=204, body={"message": "added user"})


@app.get("/users")
def trigger_job():
    return clips_service.scan()


# Register handler function
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
def lambda_handler(event: dict, context: LambdaContext):
    return app.resolve(event, context)
