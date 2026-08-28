from typing import Optional, List, Dict, Union
from listmonk_api.models import (
    SubscriberCreateRequest,
)
from listmonk_api.api.api_client_base import BaseApiClient, PaginationRequest


def _list_id_filter(list_id: Optional[Union[int, List[int]]]) -> str:
    """Build the ``&list_id=...`` query-filter suffix for one or many list ids."""
    if not list_id:
        return ""
    if isinstance(list_id, list):
        return "".join(f"&list_id={single_list_id}" for single_list_id in list_id)
    return f"&list_id={list_id}"


class ListmonkAPI(BaseApiClient):
    def get_subscribers(
        self,
        query: Optional[Dict] = None,
        list_id: Optional[Union[int, List[int]]] = None,
        max_pages: int = 0,
        per_page: int = 100,
    ):
        # BUG FIX 1: Safely get X-Total-Pages, defaulting to 1 if not present
        # (handled by BaseApiClient._paginate_results)
        return self._paginate_results(
            PaginationRequest(
                endpoint="/subscribers",
                per_page=per_page,
                max_pages=max_pages,
                extra_filter=_list_id_filter(list_id),
                data=query or None,
            )
        )

    def get_subscriber(self, subscriber_id: int):
        return self.get(f"/subscribers/{subscriber_id}").json()

    def get_subscribers_from_list(self, list_id: int):
        return self.get(f"/subscribers/lists/{list_id}").json()

    def create_subscriber(self, data: SubscriberCreateRequest):
        return self.post("/subscribers", json=data.model_dump(exclude_none=True)).json()

    # ------------------------------------------------------------------------------------------------------------------
    # Lists API
    # ------------------------------------------------------------------------------------------------------------------
