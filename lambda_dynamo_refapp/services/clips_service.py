from typing import Any

import boto3
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource, Table


class ClipsService:
    def __init__(
        self,
        clips_table: str,
        endpoint_url: str,
        aws_access_id: str,
        aws_access_key: str,
        aws_region: str,
    ):
        self.dynamo: DynamoDBServiceResource = boto3.resource(
            "dynamodb",
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_id,
            aws_secret_access_key=aws_access_key,
            region_name=aws_region,
        )
        self.clips_table: Table = self.dynamo.Table(clips_table)

    def put_clips(self, user: str, clips: list[str]) -> None:
        self.clips_table.put_item(Item={"user": user, "clips": clips})

    def scan(self) -> Any:
        return self.clips_table.scan()
