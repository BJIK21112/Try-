import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables for non-sensitive config
load_dotenv()

# Import secret manager only if in production and available, and not in testing
IS_TESTING = os.getenv("PYTEST_CURRENT_TEST") is not None or "pytest" in os.environ.get(
    "_", ""
)

try:
    if not IS_TESTING and os.getenv("GOOGLE_CLOUD_PROJECT"):
        from google.cloud import secretmanager

        secret_client: Optional[secretmanager.SecretManagerServiceClient] = (
            secretmanager.SecretManagerServiceClient()
        )
    else:
        secret_client = None
except ImportError:
    secret_client = None


def get_secret(
    secret_name: str, project_id: str = "sublime-lodge-472322-m2"
) -> Optional[str]:
    """
    Retrieve secret from Cloud Secret Manager.
    Falls back to environment variables in development.
    Returns None if secret is not available (for graceful startup).
    """
    try:
        if secret_client and os.getenv("GOOGLE_CLOUD_PROJECT"):
            # Production: Fetch from Secret Manager
            name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
            response = secret_client.access_secret_version(request={"name": name})
            return response.payload.data.decode("UTF-8")
        else:
            # Development: Use environment variables
            return os.getenv(secret_name)
    except Exception as e:
        # Log the error but don't fail startup
        print(f"Warning: Could not load secret {secret_name}: {e}")
        return None


class Config:
    # Non-sensitive configuration from environment (loaded at startup)
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", 10))
    SPAM_THRESHOLD = int(os.getenv("SPAM_THRESHOLD", 5))

    # Twitter API credentials from Secret Manager (lazy loaded)
    @property
    def TWITTER_CLIENT_ID(self) -> str:
        value = get_secret("twitter-client-id")
        if value is None:
            # Return a dummy value to allow startup, will fail when actually used
            return "dummy-client-id"
        return value

    @property
    def TWITTER_CLIENT_SECRET(self) -> str:
        value = get_secret("twitter-client-secret")
        if value is None:
            return "dummy-client-secret"
        return value

    @property
    def TWITTER_BEARER_TOKEN(self) -> str:
        value = get_secret("twitter-bearer-token")
        if value is None:
            return "dummy-bearer-token"
        return value

    @property
    def TWITTER_ACCESS_TOKEN(self) -> str:
        value = get_secret("twitter-access-token")
        if value is None:
            return "dummy-access-token"
        return value

    @property
    def TWITTER_ACCESS_TOKEN_SECRET(self) -> str:
        value = get_secret("twitter-access-token-secret")
        if value is None:
            return "dummy-access-token-secret"
        return value

    @property
    def COINGECKO_API_KEY(self) -> Optional[str]:
        value = get_secret("coingecko-api-key")
        if value is None:
            return None  # CoinGecko API key is optional
        return value


# Create a global config instance
config = Config()
