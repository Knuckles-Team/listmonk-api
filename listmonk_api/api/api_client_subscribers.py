from typing import Optional, List, Dict, Union
from listmonk_api.models import (
    SubscriberCreateRequest,
)
from listmonk_api.api.api_client_base import BaseApiClient


class ListmonkAPI(BaseApiClient):
    def get_subscribers(
        self,
        query: Optional[Dict] = None,
        list_id: Optional[Union[int, List[int]]] = None,
        max_pages: int = 0,
        per_page: int = 100,
    ):
        # Fetch the first page to get X-Total-Pages
        response = self.get(f"/subscribers?per_page={per_page}")
        # BUG FIX 1: Safely get X-Total-Pages, defaulting to 1 if not present
        total_pages = int(response.headers.get("X-Total-Pages", 1))

        results = []
        subscriber_filter = f"?per_page={per_page}"

        if list_id:
            if isinstance(list_id, list):
                for single_list_id in list_id:
                    subscriber_filter += f"&list_id={single_list_id}"
            else:
                subscriber_filter += f"&list_id={list_id}"

        if max_pages == 0 or max_pages > total_pages:
            max_pages = total_pages

        data = None
        if query:
            data = query

        for page in range(1, max_pages + 1):
            # Listmonk usually uses 1-indexed pages for its endpoints like `?page=1`
            response_page = self.get(
                f"/subscribers{subscriber_filter}&page={page}", json=data
            )
            response_json = response_page.json()
            if isinstance(response_json, dict) and "data" in response_json:
                results.extend(response_json["data"].get("results", []))
            elif isinstance(response_json, list):
                results.extend(response_json)
            else:
                results.append(response_json)

        return results

    def get_subscriber(self, subscriber_id: int):
        return self.get(f"/subscribers/{subscriber_id}").json()

    def get_subscribers_from_list(self, list_id: int):
        return self.get(f"/subscribers/lists/{list_id}").json()

    def create_subscriber(self, data: SubscriberCreateRequest):
        return self.post("/subscribers", json=data.model_dump(exclude_none=True)).json()

    # ------------------------------------------------------------------------------------------------------------------
    # Lists API
    # ------------------------------------------------------------------------------------------------------------------
