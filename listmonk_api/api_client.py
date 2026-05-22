from typing import Optional, List, Dict, Union
import requests

from listmonk_api.models import (
    SubscriberCreateRequest,
    ListCreateRequest,
    ListEditRequest,
    ImportSubscribersRequest,
    CampaignCreateRequest,
    CampaignStatusRequest,
    MediaUploadRequest,
    TransactionalMessageRequest,
)


class ListmonkAPI:
    """API client for Listmonk."""

    def __init__(self, url: str, token: str):
        self.base_url = url
        self._session = requests.Session()
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

    # ------------------------------------------------------------------------------------------------------------------
    # Subscribers API
    # ------------------------------------------------------------------------------------------------------------------
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
    def get_media(self, media_id: int):
        return self.get("/media").json()

    def upload_media(self, data: MediaUploadRequest):
        return self.post("/media", json=data.model_dump(exclude_none=True)).json()

    def delete_media(self, media_id: int):
        return self.delete(f"/media/{media_id}").json()

    # ------------------------------------------------------------------------------------------------------------------
    # Templates API
    # ------------------------------------------------------------------------------------------------------------------
    def get_templates(self, max_pages: int = 0, per_page: int = 100):
        response = self.get(f"/templates?per_page={per_page}")
        total_pages = int(response.headers.get("X-Total-Pages", 1))

        results = []
        template_filter = f"?per_page={per_page}"

        if max_pages == 0 or max_pages > total_pages:
            max_pages = total_pages

        for page in range(1, max_pages + 1):
            response_page = self.get(f"/templates{template_filter}&page={page}")
            response_json = response_page.json()
            if isinstance(response_json, dict) and "data" in response_json:
                results.extend(response_json["data"].get("results", []))
            elif isinstance(response_json, list):
                results.extend(response_json)
            else:
                results.append(response_json)

        return results

    def get_template(self, template_id: int):
        return self.get(f"/templates/{template_id}").json()

    def get_template_preview(self, template_id: int):
        return self.get(f"/templates/{template_id}/preview").json()

    def set_default_template(self, template_id: int):
        return self.put(f"/templates/{template_id}/default").json()

    def delete_template(self, template_id: int):
        return self.delete(f"/templates/{template_id}").json()

    # ------------------------------------------------------------------------------------------------------------------
    # Transactional API
    # ------------------------------------------------------------------------------------------------------------------
    def transactional_message(self, data: TransactionalMessageRequest):
        # BUG FIX 4: Included attachments in data model and excluded None
        return self.post("/tx", json=data.model_dump(exclude_none=True)).json()
