from pydantic import BaseModel


class UserRequest(BaseModel):
    user: str


class ClipsInfo(BaseModel):
    id: str
    url: str
    embed_url: str
    broadcaster_id: str
    broadcaster_name: str
    creator_id: str
    creator_name: str
    video_id: str
    game_id: str
    language: str
    title: str
    view_count: int
    created_at: str
    thumbnail_url: str
    duration: float
    vod_offset: int
    is_featured: bool


class Pagination(BaseModel):
    cursor: str


class ClipsResponse(BaseModel):
    data: list[ClipsInfo]
    pagination: Pagination
