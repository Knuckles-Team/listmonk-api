import requests


class BaseApiClient:
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
