import os
from aws_lambda_powertools.event_handler import ALBResolver

from aws_lambda_powertools import Logger
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

from lambda_dynamo_refapp.services.twitch_service import TwitchService
from lambda_dynamo_refapp.models.twitch import UserRequest
from lambda_dynamo_refapp.services.clips_service import ClipsService

logger = Logger()
app = ALBResolver(enable_validation=True)

# Load Env
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
clips_table = os.getenv("DYNAMO_TABLE")
aws_access_id = os.getenv("AWS_ACCESS_ID")
aws_access_key = os.getenv("AWS_ACCESS_KEY")
endpoint_url = os.getenv("ENDPOINT_URL")
aws_region = os.getenv("AWS_REGION")

if (
    client_id is None
    or client_secret is None
    or clips_table is None
    or aws_access_id is None
    or aws_access_key is None
    or endpoint_url is None
    or aws_region is None
):
    raise ValueError("Found empty client_id or client_secret")

twitch_service = TwitchService(client_id, client_secret)
clips_service = ClipsService(
    clips_table, endpoint_url, aws_access_id, aws_access_key, aws_region
)


@app.get("/health")
def get_health() -> dict:
    return {"message": "Looks like things are up and running!"}


@app.post("/user")
def post_user(request: UserRequest) -> dict:
    clips = twitch_service.get_clips_from_broadcaster(request.user)
    clips_service.put_clips(request.user, clips)
    return {"messsage": "Successflly created the table!"}


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
def lambda_handler(event: dict, context: LambdaContext):
    return app.resolve(event, context)
