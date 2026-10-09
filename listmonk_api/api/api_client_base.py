from dataclasses import dataclass, field
from typing import Any, Optional

import requests
from agent_connector_sdk.tls.profile import ResolvedTLSProfile
from agent_connector_sdk.tls.resolve import resolve_tls_profile


@dataclass(frozen=True)
class PaginationRequest:
    """Parameters for one :meth:`BaseApiClient._paginate_results` call."""

    endpoint: str
    per_page: int
    max_pages: int
    extra_filter: str = ""
    order_by: Optional[str] = None
    order: Optional[str] = None
    valid_order_by: tuple = field(default_factory=tuple)
    data: Optional[dict] = None


def _flatten_page_results(response_json: Any) -> list:
    """Normalize one paginated-list response page into a flat list of records.

    Handles the three shapes Listmonk's list endpoints return: a
    ``{"data": {"results": [...]}}`` envelope, a bare list, or any other
    JSON value (kept as a single-item result).
    """
    if isinstance(response_json, dict) and "data" in response_json:
        return list(response_json["data"].get("results", []))
    if isinstance(response_json, list):
        return list(response_json)
    return [response_json]


class BaseApiClient:
    def __init__(
        self,
        url: str,
        token: str,
        tls_profile: ResolvedTLSProfile | None = None,
    ):
        self.base_url = url
        self._session = requests.Session()
        self.tls_profile = tls_profile or resolve_tls_profile("listmonk")
        self.tls_profile.configure_requests_session(self._session)
        self._session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
        )

    def get(self, endpoint: str, **kwargs):
        url = self.base_url.rstrip("/") + "/" + endpoint.lstrip("/")
        response = self._session.get(url, **kwargs)
        response.raise_for_status()
        return response

    def post(self, endpoint: str, **kwargs):
        url = self.base_url.rstrip("/") + "/" + endpoint.lstrip("/")
        response = self._session.post(url, **kwargs)
        response.raise_for_status()
        return response

    def put(self, endpoint: str, **kwargs):
        url = self.base_url.rstrip("/") + "/" + endpoint.lstrip("/")
        response = self._session.put(url, **kwargs)
        response.raise_for_status()
        return response

    def delete(self, endpoint: str, **kwargs):
        url = self.base_url.rstrip("/") + "/" + endpoint.lstrip("/")
        response = self._session.delete(url, **kwargs)
        response.raise_for_status()
        return response

    def _paginate_results(self, request: PaginationRequest) -> list:
        """Fetch every page of a Listmonk list endpoint and flatten the results.

        Shared by ``get_campaigns``/``get_lists``/``get_subscribers``: fetches
        page 1 to read ``X-Total-Pages``, builds
        ``?per_page=<n><extra_filter><&order_by=...><&order=...>&page=<i>``,
        and flattens each page via :func:`_flatten_page_results`.
        """
        endpoint = request.endpoint
        per_page = request.per_page
        response = self.get(f"{endpoint}?per_page={per_page}")
        total_pages = int(response.headers.get("X-Total-Pages", 1))

        filter_str = f"?per_page={per_page}{request.extra_filter}"
        if request.order_by and request.order_by in request.valid_order_by:
            filter_str += f"&order_by={request.order_by}"
        if request.order and request.order.upper() in ("ASC", "DESC"):
            filter_str += f"&order={request.order}"

        max_pages = request.max_pages
        if max_pages == 0 or max_pages > total_pages:
            max_pages = total_pages

        results: list = []
        for page in range(1, max_pages + 1):
            response_page = self.get(
                f"{endpoint}{filter_str}&page={page}", json=request.data
            )
            results.extend(_flatten_page_results(response_page.json()))
        return results
