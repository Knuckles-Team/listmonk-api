from listmonk_api.api.api_client_base import BaseApiClient, PaginationRequest
from listmonk_api.models import (
    ListCreateRequest,
    ListEditRequest,
)


class ListmonkAPI(BaseApiClient):
    def get_lists(
        self,
        query: dict | None = None,
        order_by: str | None = None,
        order: str | None = None,
        max_pages: int = 0,
        per_page: int = 100,
    ):
        return self._paginate_results(
            PaginationRequest(
                endpoint="/lists",
                per_page=per_page,
                max_pages=max_pages,
                order_by=order_by,
                order=order,
                valid_order_by=("name", "status", "created_at", "updated_at"),
                data=query or None,
            )
        )

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
