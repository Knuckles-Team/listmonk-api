from typing import Optional, Dict
from listmonk_api.models import (
    ListCreateRequest,
    ListEditRequest,
)
from listmonk_api.api.api_client_base import BaseApiClient


class ListmonkAPI(BaseApiClient):
    def get_lists(
        self,
        query: Optional[Dict] = None,
        order_by: Optional[str] = None,
        order: Optional[str] = None,
        max_pages: int = 0,
        per_page: int = 100,
    ):
        response = self.get(f"/lists?per_page={per_page}")
        total_pages = int(response.headers.get("X-Total-Pages", 1))

        results = []
        list_filter = f"?per_page={per_page}"

        if order_by and order_by in ["name", "status", "created_at", "updated_at"]:
            list_filter += f"&order_by={order_by}"
        if order and order.upper() in ["ASC", "DESC"]:
            list_filter += f"&order={order}"

        if max_pages == 0 or max_pages > total_pages:
            max_pages = total_pages

        data = None
        if query:
            data = query

        for page in range(1, max_pages + 1):
            response_page = self.get(f"/lists{list_filter}&page={page}", json=data)
            response_json = response_page.json()
            if isinstance(response_json, dict) and "data" in response_json:
                results.extend(response_json["data"].get("results", []))
            elif isinstance(response_json, list):
                results.extend(response_json)
            else:
                results.append(response_json)

        return results

    def get_list(self, list_id: int):
        return self.get(f"/lists/{list_id}").json()

    def create_list(self, data: ListCreateRequest):
        return self.post("/lists", json=data.model_dump(exclude_none=True)).json()

    def edit_list(self, list_id: int, data: ListEditRequest):
        return self.put(
            f"/lists/{list_id}", json=data.model_dump(exclude_none=True)
        ).json()

    # ------------------------------------------------------------------------------------------------------------------
    # Import API
    # ------------------------------------------------------------------------------------------------------------------
