from typing import Any

import boto3


class ClipsService:
    def __init__(self, clips_table: Any):
        self.clips_table = boto3.resource("dynamodb").Table(clips_table)

    def put_clips(self, user: str, clips: list[str]) -> None:
        self.clips_table.put_item(Item={"user": user, "clips": clips})

    def scan(self) -> Any:
        return self.clips_table.scan()
