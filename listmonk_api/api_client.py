from listmonk_api.api.api_client_campaigns import ListmonkAPI as CampaignsApi
from listmonk_api.api.api_client_import_api import ListmonkAPI as ImportApi
from listmonk_api.api.api_client_lists import ListmonkAPI as ListsApi
from listmonk_api.api.api_client_media import ListmonkAPI as MediaApi
from listmonk_api.api.api_client_subscribers import ListmonkAPI as SubscribersApi
from listmonk_api.api.api_client_templates import ListmonkAPI as TemplatesApi
from listmonk_api.api.api_client_transactional import ListmonkAPI as TransactionalApi


class ListmonkAPI(
    CampaignsApi,
    ImportApi,
    ListsApi,
    MediaApi,
    SubscribersApi,
    TemplatesApi,
    TransactionalApi,
):
    """API client for Listmonk."""

    pass
