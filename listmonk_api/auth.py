#!/usr/bin/python
# coding: utf-8

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from agent_utilities.core.config import setting
from agent_utilities.core.exceptions import AuthError, UnauthorizedError

from listmonk_api.api_client import ListmonkAPI

_client = None


def get_client():
    """Get or create a singleton API client instance."""
    global _client
    if _client is None:
        base_url = setting("LISTMONK_URL", "http://localhost:8080")
        token = setting("LISTMONK_TOKEN", "")

        try:
            _client = ListmonkAPI(
                url=base_url,
                token=token,
            )

        except (AuthError, UnauthorizedError) as e:
            raise RuntimeError(
                f"AUTHENTICATION ERROR: The credentials provided are not valid for '{base_url}'. "
                f"Please check your LISTMONK_TOKEN and LISTMONK_URL environment variables. "
                f"Error details: {str(e)}"
            ) from e

    return _client
