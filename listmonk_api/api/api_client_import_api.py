from listmonk_api.models import (
    ImportSubscribersRequest,
)
from listmonk_api.api.api_client_base import BaseApiClient


class ListmonkAPI(BaseApiClient):
    def get_subscriber_import_status(self):
        return self.get("/import/subscribers").json()

    def get_subscriber_import_logs(self):
        return self.get("/import/subscribers/logs").json()

    def import_subscribers(self, data: ImportSubscribersRequest):
        # NOTE: Using self.post instead of self.get for importing as it was incorrect in the old wrapper.
        # Actually listmonk expects a POST for import
        return self.post(
            "/import/subscribers", json=data.model_dump(exclude_none=True)
        ).json()

    def delete_subscriber_import(self):
        return self.delete("/import/subscribers/logs").json()

    # ------------------------------------------------------------------------------------------------------------------
    # Campaigns API
    # ------------------------------------------------------------------------------------------------------------------
