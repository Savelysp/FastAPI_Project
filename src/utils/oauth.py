from authlib.integrations.starlette_client import OAuth

from src.settings import settings

__all__ = [
    "oauth"
]

oauth = OAuth()

oauth.register(
    name="google",
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=settings.OAUTH_CLIENT_ID.get_secret_value(),
    client_secret=settings.OAUTH_CLIENT_SECRET.get_secret_value(),
    client_kwargs={
        'scope': 'email openid profile',
    }
)
