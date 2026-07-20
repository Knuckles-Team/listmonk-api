from agent_utilities.core.config import setting
from agent_utilities.core.exceptions import AuthError, UnauthorizedError
from agent_utilities.core.transport_security import resolve_configured_tls_profile

from listmonk_api.api_client import ListmonkAPI

_client = None


def get_client():
    """Get or create a singleton API client instance."""
    global _client
    if _client is None:
        base_url = setting("LISTMONK_URL", "https://listmonk.example.invalid")
        token = setting("LISTMONK_TOKEN", "")
        tls_profile = resolve_configured_tls_profile(
            "listmonk",
            profile_name=setting("LISTMONK_TLS_PROFILE", "") or None,
            profile_ref=setting("LISTMONK_TLS_PROFILE_REF", "") or None,
        )

        try:
            _client = ListmonkAPI(
                url=base_url,
                token=token,
                tls_profile=tls_profile,
            )

        except (AuthError, UnauthorizedError) as e:
            raise RuntimeError(
                "AUTHENTICATION ERROR: The configured credentials were rejected. "
                f"Please check your LISTMONK_TOKEN and LISTMONK_URL environment variables. "
                f"Error details: {type(e).__name__}"
            ) from e

    return _client
