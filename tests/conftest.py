import pytest
import os
from unittest.mock import patch, MagicMock


@pytest.fixture(autouse=True)
def mock_google_cloud():
    """Mock Google Cloud services for testing"""
    with patch("google.cloud.secretmanager.SecretManagerServiceClient") as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance

        # Mock the access_secret_version method
        mock_response = MagicMock()
        mock_response.payload.data.decode.return_value = "mock_secret_value"
        mock_instance.access_secret_version.return_value = mock_response

        yield mock_instance


@pytest.fixture(autouse=True)
def mock_google_logging():
    """Mock Google Cloud Logging for testing"""
    with (
        patch("google.cloud.logging.Client"),
        patch("google.cloud.logging.handlers.CloudLoggingHandler"),
    ):
        yield


@pytest.fixture(autouse=True)
def test_env():
    """Set up test environment variables"""
    # Ensure we're not in production mode during tests
    old_value = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if "GOOGLE_CLOUD_PROJECT" in os.environ:
        del os.environ["GOOGLE_CLOUD_PROJECT"]

    yield

    # Restore original value
    if old_value:
        os.environ["GOOGLE_CLOUD_PROJECT"] = old_value
