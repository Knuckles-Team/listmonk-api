import requests
from agent_utilities.core.transport_security import (
    ResolvedTLSProfile,
    resolve_configured_tls_profile,
)


class BaseApiClient:
    def __init__(
        self,
        url: str,
        token: str,
        tls_profile: ResolvedTLSProfile | None = None,
    ):
        self.base_url = url
        self._session = requests.Session()
        self.tls_profile = tls_profile or resolve_configured_tls_profile("listmonk")
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
