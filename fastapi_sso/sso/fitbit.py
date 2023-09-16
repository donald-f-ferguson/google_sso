"""Fitbit OAuth Login Helper
"""

from fastapi_sso.sso.base import DiscoveryDocument, OpenID, SSOBase, SSOLoginError


class FitbitSSO(SSOBase):
    """Class providing login via Fitbit OAuth"""

    provider = "fitbit"
    scope = ["profile"]

    @classmethod
    async def openid_from_response(cls, response: dict) -> OpenID:
        """Return OpenID from user information provided by Google"""
        info = response.get("user")
        if not info:
            raise SSOLoginError(401, "Failed to process login via Fitbit")
        return OpenID(
            id=info["encodedId"],
            first_name=info["fullName"],
            display_name=info["displayName"],
            picture=info["avatar"],
            provider=cls.provider,
        )

    async def get_discovery_document(self) -> DiscoveryDocument:
        """Get document containing handy urls"""
        return {
            "authorization_endpoint": "https://www.fitbit.com/oauth2/authorize?response_type=code",
            "token_endpoint": "https://api.fitbit.com/oauth2/token",
            "userinfo_endpoint": "https://api.fitbit.com/1/user/-/profile.json",
        }
