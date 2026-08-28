from typing import Optional, Dict
from listmonk_api.models import (
    CampaignCreateRequest,
    CampaignStatusRequest,
)
from listmonk_api.api.api_client_base import BaseApiClient, PaginationRequest


class ListmonkAPI(BaseApiClient):
    def get_campaigns(
        self,
        query: Optional[Dict] = None,
        order_by: Optional[str] = None,
        order: Optional[str] = None,
        max_pages: int = 0,
        per_page: int = 100,
    ):
        return self._paginate_results(
            PaginationRequest(
                endpoint="/campaigns",
                per_page=per_page,
                max_pages=max_pages,
                order_by=order_by,
                order=order,
                valid_order_by=("name", "status", "created_at", "updated_at"),
                data=query or None,
            )
        )

    def get_campaign(self, campaign_id: int):
        return self.get(f"/campaigns/{campaign_id}").json()

    def get_campaign_preview(self, campaign_id: int):
        return self.get(f"/campaigns/{campaign_id}/preview").json()

    def get_campaign_stats(self, campaign_id: int):
        return self.get(f"/campaigns/{campaign_id}/running/stats").json()

    def create_campaign(self, data: CampaignCreateRequest):
        # BUG FIX 2 & 3: Included attachments in data model and mapped send_type to type via pydantic alias (by_alias=True)
        return self.post(
            "/campaigns", json=data.model_dump(by_alias=True, exclude_none=True)
        ).json()

    def set_campaign_status(self, campaign_id: int, data: CampaignStatusRequest):
        return self.put(
            f"/campaigns/{campaign_id}/status", json=data.model_dump(exclude_none=True)
        ).json()

    def delete_campaign(self, campaign_id: int):
        return self.delete(f"/campaigns/{campaign_id}").json()

    # ------------------------------------------------------------------------------------------------------------------
    # Media API
    # ------------------------------------------------------------------------------------------------------------------
