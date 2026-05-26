from listmonk_api.models import (
    MediaUploadRequest,
)
from listmonk_api.api.api_client_base import BaseApiClient


class ListmonkAPI(BaseApiClient):
    def get_media(self, media_id: int):
        return self.get("/media").json()

    def upload_media(self, data: MediaUploadRequest):
        return self.post("/media", json=data.model_dump(exclude_none=True)).json()

    def delete_media(self, media_id: int):
        return self.delete(f"/media/{media_id}").json()

    # ------------------------------------------------------------------------------------------------------------------
    # Templates API
    # ------------------------------------------------------------------------------------------------------------------
