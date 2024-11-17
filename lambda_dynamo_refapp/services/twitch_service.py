import time

import httpx
from httpx import Client, Response

from lambda_dynamo_refapp.models.twitch import ClipsResponse


class TwitchService:
    _oauth_url: str = "https://id.twitch.tv/oauth2/token"
    _helix_api_url: str = "https://api.twitch.tv/helix/"
    _user_endpoint: str = "users"
    _clips_endpoint: str = "clips"

    def __init__(self, client_id: str, client_secret: str):
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.grant_type: str = "client_credentials"
        self.token: str = ""
        self.token_created_time: float = 0.0
        self.token_expiration: float = 0.0

    def get_clips_from_broadcaster(self, username: str) -> list[str]:
        self._refresh_token()
        broadcaster_id = self._get_broadcaster_id(username)
        clips = self._get_clips(broadcaster_id)
        return TwitchService.extract_clips(clips)

    @staticmethod
    def extract_clips(clips_response: ClipsResponse) -> list[str]:
        return [clip.url for clip in clips_response.data]

    def _refresh_token(self):
        if not self.token:
            print("No token found, creating a new oauth token")
            self._get_oauth()

        if time.time() - self.token_created_time > self.token_expiration:
            print("OAuth token expired, creating a new oauth token")
            self._get_oauth()

    def _get_oauth(self):
        try:
            params = self._get_oauth_query_params()
            response = httpx.post(TwitchService._oauth_url, params=params)
            response_dict = response.json()
            self.token = response_dict["access_token"]
            self.token_expiration = float(response_dict["expires_in"])
            self.token_created_time = time.time()
        except httpx.RequestError as exc:
            print(f"An error occurred while requesting {exc.request.url}.")
            raise exc
        except httpx.HTTPStatusError as exc:
            print(
                f"Error response {exc.response.status_code} while requesting {exc.request.url}."
            )
            raise exc

    def _get_oauth_query_params(self) -> dict[str, str]:
        return {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": self.grant_type,
        }

    def _get_oauth_headers(self) -> dict[str, str]:
        return {"Authorization": "Bearer " + self.token, "Client-Id": self.client_id}

    def _get_broadcaster_id(self, username: str) -> str:
        query_params = {"login": username}
        response = self._send_get_request(
            endpoint=TwitchService._user_endpoint, query_params=query_params
        )
        print(
            f"When fetching broadcaster_id, received a valid response: {response.json()}"
        )
        return response.json()["data"][0]["id"]

    def _get_clips(self, broadcaster_id: str) -> ClipsResponse:
        query_params = {"broadcaster_id": broadcaster_id}
        response = self._send_get_request(
            endpoint=TwitchService._clips_endpoint, query_params=query_params
        )
        print(f"When fetching user clips, received a valid response: {response.json()}")
        return ClipsResponse(**response.json())

    def _send_get_request(
        self, endpoint: str, query_params: dict[str, str]
    ) -> Response:
        headers = self._get_oauth_headers()
        try:
            with Client(base_url=TwitchService._helix_api_url) as client:
                return client.get(
                    headers=headers,
                    params=query_params,
                    url=endpoint,
                )
        except httpx.RequestError as exc:
            print(f"An error occurred while requesting {exc.request.url!r}.")
            raise exc
        except httpx.HTTPStatusError as exc:
            print(
                f"Error response {exc.response.status_code} while requesting {exc.request.url!r}."
            )
            raise exc
