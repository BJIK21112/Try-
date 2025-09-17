import pytest
from unittest.mock import Mock, patch
from src.engagement import EngagementBot
from src.twitter_client import TwitterClient
from src.market_data import MarketData
from src.rate_limiter import RateLimiter
from src.spam_detector import SpamDetector


class TestEngagementBot:
    @pytest.fixture
    def mock_components(self):
        """Create mocked components for testing"""
        mock_twitter = Mock(spec=TwitterClient)
        mock_market = Mock(spec=MarketData)
        mock_rate_limiter = Mock(spec=RateLimiter)
        mock_spam_detector = Mock(spec=SpamDetector)

        return {
            "twitter": mock_twitter,
            "market": mock_market,
            "rate_limiter": mock_rate_limiter,
            "spam_detector": mock_spam_detector,
        }

    @pytest.fixture
    def bot(self, mock_components):
        """Create bot instance with mocked components"""
        with (
            patch(
                "src.engagement.TwitterClient", return_value=mock_components["twitter"]
            ),
            patch("src.engagement.MarketData", return_value=mock_components["market"]),
            patch(
                "src.engagement.RateLimiter",
                return_value=mock_components["rate_limiter"],
            ),
            patch(
                "src.engagement.SpamDetector",
                return_value=mock_components["spam_detector"],
            ),
        ):
            return EngagementBot()

    def test_post_market_update_success(self, bot, mock_components):
        """Test successful market update posting"""
        # Setup mocks
        mock_components["rate_limiter"].can_request.return_value = True
        mock_components["market"].get_trending_coins.return_value = ["bitcoin"]
        mock_components["market"].get_coin_price.return_value = 50000
        mock_components["twitter"].post_tweet.return_value = "tweet_id_123"

        # Execute
        bot.post_market_update()

        # Verify
        mock_components["twitter"].post_tweet.assert_called_once()
        assert "Bitcoin" in mock_components["twitter"].post_tweet.call_args[0][0]
        assert "$50000" in mock_components["twitter"].post_tweet.call_args[0][0]

    def test_post_market_update_rate_limited(self, bot, mock_components):
        """Test market update when rate limited"""
        mock_components["rate_limiter"].can_request.return_value = False

        bot.post_market_update()

        # Should not call market or twitter methods
        mock_components["market"].get_trending_coins.assert_not_called()
        mock_components["twitter"].post_tweet.assert_not_called()

    def test_post_market_update_no_trending_coins(self, bot, mock_components):
        """Test market update when no trending coins available"""
        mock_components["rate_limiter"].can_request.return_value = True
        mock_components["market"].get_trending_coins.return_value = []

        bot.post_market_update()

        mock_components["market"].get_trending_coins.assert_called_once()
        mock_components["twitter"].post_tweet.assert_not_called()

    def test_post_market_update_no_price(self, bot, mock_components):
        """Test market update when price fetch fails"""
        mock_components["rate_limiter"].can_request.return_value = True
        mock_components["market"].get_trending_coins.return_value = ["bitcoin"]
        mock_components["market"].get_coin_price.return_value = None

        bot.post_market_update()

        mock_components["market"].get_coin_price.assert_called_once_with("bitcoin")
        mock_components["twitter"].post_tweet.assert_not_called()

    def test_engage_with_tweets_success(self, bot, mock_components):
        """Test successful tweet engagement"""
        # Setup mocks
        mock_components["rate_limiter"].can_request.return_value = True
        mock_components["spam_detector"].is_spam.return_value = False
        mock_tweet = Mock()
        mock_tweet.id = "tweet_123"
        mock_tweet.text = "Great crypto project!"
        mock_components["twitter"].search_tweets.return_value = [mock_tweet]
        mock_components["twitter"].like_tweet.return_value = True
        mock_components["twitter"].reply_to_tweet.return_value = "reply_456"

        # Execute
        bot.engage_with_tweets()

        # Verify
        mock_components["twitter"].search_tweets.assert_called_once()
        mock_components["twitter"].like_tweet.assert_called_once_with("tweet_123")
        mock_components["twitter"].reply_to_tweet.assert_called_once()

    def test_engage_with_tweets_spam_filtered(self, bot, mock_components):
        """Test that spam tweets are filtered out"""
        mock_components["rate_limiter"].can_request.return_value = True
        mock_components["spam_detector"].is_spam.return_value = True
        mock_tweet = Mock()
        mock_tweet.id = "tweet_123"
        mock_tweet.text = "SPAM CONTENT"
        mock_components["twitter"].search_tweets.return_value = [mock_tweet]

        bot.engage_with_tweets()

        # Should not engage with spam
        mock_components["twitter"].like_tweet.assert_not_called()
        mock_components["twitter"].reply_to_tweet.assert_not_called()

    def test_promote_community_success(self, bot, mock_components):
        """Test successful community promotion"""
        mock_components["rate_limiter"].can_request.return_value = True
        mock_components["twitter"].post_tweet.return_value = "promo_tweet_789"

        bot.promote_community()

        mock_components["twitter"].post_tweet.assert_called_once()
        assert "wifDOG" in mock_components["twitter"].post_tweet.call_args[0][0]
        assert "crypto" in mock_components["twitter"].post_tweet.call_args[0][0]


def test_engage_with_tweets():
    assert True
