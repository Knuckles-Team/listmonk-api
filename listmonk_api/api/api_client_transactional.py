from listmonk_api.models import (
    TransactionalMessageRequest,
)
from listmonk_api.api.api_client_base import BaseApiClient


class ListmonkAPI(BaseApiClient):
    def transactional_message(self, data: TransactionalMessageRequest):
        # BUG FIX 4: Included attachments in data model and excluded None
        return self.post("/tx", json=data.model_dump(exclude_none=True)).json()
