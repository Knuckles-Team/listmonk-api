from typing import Optional, Dict
from listmonk_api.models import (
    CampaignCreateRequest,
    CampaignStatusRequest,
)
from listmonk_api.api.api_client_base import BaseApiClient


class ListmonkAPI(BaseApiClient):
    def get_campaigns(
        self,
        query: Optional[Dict] = None,
        order_by: Optional[str] = None,
        order: Optional[str] = None,
        max_pages: int = 0,
        per_page: int = 100,
    ):
        response = self.get(f"/campaigns?per_page={per_page}")
        total_pages = int(response.headers.get("X-Total-Pages", 1))

        results = []
        campaign_filter = f"?per_page={per_page}"

        if order_by and order_by in ["name", "status", "created_at", "updated_at"]:
            campaign_filter += f"&order_by={order_by}"
        if order and order.upper() in ["ASC", "DESC"]:
            campaign_filter += f"&order={order}"

        if max_pages == 0 or max_pages > total_pages:
            max_pages = total_pages

        data = None
        if query:
            data = query

        for page in range(1, max_pages + 1):
            response_page = self.get(
                f"/campaigns{campaign_filter}&page={page}", json=data
            )
            response_json = response_page.json()
            if isinstance(response_json, dict) and "data" in response_json:
                results.extend(response_json["data"].get("results", []))
            elif isinstance(response_json, list):
                results.extend(response_json)
            else:
                results.append(response_json)

        return results

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
