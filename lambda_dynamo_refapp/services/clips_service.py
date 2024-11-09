from typing import Any


class ClipsService:
    def __init__(self, clips_table: Any):
        self.clips_table = clips_table

    def put_clips(self, user: str, clips: list[str]) -> None:
        self.clips_table.put_item(Item={"user": user, "clips": clips})

    def scan(self) -> Any:
        return self.clips_table.scan()
