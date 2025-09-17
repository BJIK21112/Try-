import os
import pytest
from unittest.mock import patch
from src.market_data import MarketData


class TestMarketData:
    @pytest.fixture
    def market_data(self):
        """Create MarketData instance"""
        return MarketData()

    def test_get_trending_coins_success(self, market_data):
        """Test successful trending coins fetch"""
        mock_response = {
            "coins": [
                {"item": {"id": "bitcoin"}},
                {"item": {"id": "ethereum"}},
                {"item": {"id": "cardano"}},
            ]
        }

        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = mock_response

            result = market_data.get_trending_coins()

            assert result == ["bitcoin", "ethereum", "cardano"]
            mock_get.assert_called_once()

    def test_get_trending_coins_failure(self, market_data):
        """Test trending coins fetch failure"""
        with patch("requests.get") as mock_get:
            mock_get.side_effect = Exception("API Error")

            result = market_data.get_trending_coins()

            assert result == []

    def test_get_coin_price_success(self, market_data):
        """Test successful coin price fetch"""
        mock_response = {"bitcoin": {"usd": 45000.50}}

        with (
            patch("requests.get") as mock_get,
            patch.dict(os.environ, {"coingecko-api-key": "test_key"}),
        ):
            mock_get.return_value.json.return_value = mock_response

            result = market_data.get_coin_price("bitcoin")

            assert result == 45000.50
            # Verify API key is included in request
            call_args = mock_get.call_args
            assert "x-cg-demo-api-key" in call_args[1]["headers"]

    def test_get_coin_price_without_api_key(self, market_data):
        """Test coin price fetch without API key"""
        mock_response = {"bitcoin": {"usd": 45000.50}}

        with (
            patch("requests.get") as mock_get,
            patch.dict(os.environ, {}, clear=True),
        ):
            mock_get.return_value.json.return_value = mock_response

            result = market_data.get_coin_price("bitcoin")

            assert result == 45000.50
            # Verify no API key header when None
            call_args = mock_get.call_args
            assert "x-cg-demo-api-key" not in call_args[1]["headers"]

    def test_get_coin_price_failure(self, market_data):
        """Test coin price fetch failure"""
        with patch("requests.get") as mock_get:
            mock_get.side_effect = Exception("API Error")

            result = market_data.get_coin_price("bitcoin")

            assert result is None
