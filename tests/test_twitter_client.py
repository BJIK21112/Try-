import os
import pytest
from unittest.mock import Mock, patch
from src.twitter_client import TwitterClient


class TestTwitterClient:
    @pytest.fixture
    def mock_tweepy_api(self):
        """Mock Tweepy API for testing"""
        mock_api = Mock()
        mock_api.verify_credentials.return_value = True
        return mock_api

    @pytest.fixture
    def twitter_client(self, mock_tweepy_api):
        """Create TwitterClient with mocked API"""
        with (
            patch("tweepy.Client") as mock_client_class,
            patch("tweepy.API") as mock_api_class,
            patch.dict(
                os.environ,
                {
                    "TWITTER_BEARER_TOKEN": "test_bearer",
                    "TWITTER_CLIENT_ID": "test_client_id",
                    "TWITTER_CLIENT_SECRET": "test_client_secret",
                    "TWITTER_ACCESS_TOKEN": "test_access_token",
                    "TWITTER_ACCESS_TOKEN_SECRET": "test_access_secret",
                },
            ),
        ):
            mock_client_class.return_value = mock_tweepy_api
            mock_api_class.return_value = mock_tweepy_api

            client = TwitterClient()
            yield client

    def test_initialization(self, twitter_client):
        """Test Twitter client initializes correctly"""
        assert twitter_client is not None
        assert hasattr(twitter_client, "client")
        # Note: TwitterClient only has client, not api

    def test_post_tweet_success(self, twitter_client, mock_tweepy_api):
        """Test successful tweet posting"""
        mock_response = Mock()
        mock_response.data = {"id": "1234567890"}
        mock_tweepy_api.create_tweet.return_value = mock_response

        result = twitter_client.post_tweet("Test tweet")

        assert result == "1234567890"
        mock_tweepy_api.create_tweet.assert_called_once_with(text="Test tweet")

    def test_post_tweet_failure(self, twitter_client, mock_tweepy_api):
        """Test tweet posting failure"""
        mock_tweepy_api.create_tweet.side_effect = Exception("API Error")

        result = twitter_client.post_tweet("Test tweet")

        assert result is None

    def test_like_tweet_success(self, twitter_client, mock_tweepy_api):
        """Test successful tweet liking"""
        mock_tweepy_api.like.return_value = True

        result = twitter_client.like_tweet("1234567890")

        assert result is None  # like_tweet doesn't return a value
        mock_tweepy_api.like.assert_called_once_with("1234567890")
        mock_tweepy_api.like.assert_called_once()

    def test_reply_to_tweet_success(self, twitter_client, mock_tweepy_api):
        """Test successful tweet reply"""
        mock_response = Mock()
        mock_response.data = {"id": "9876543210"}
        mock_tweepy_api.create_tweet.return_value = mock_response

        result = twitter_client.reply_to_tweet("1234567890", "Great post!")

        assert result == "9876543210"
        mock_tweepy_api.create_tweet.assert_called_once()

    def test_search_tweets(self, twitter_client, mock_tweepy_api):
        """Test tweet searching"""
        mock_tweets = [Mock(), Mock()]
        mock_tweepy_api.search_recent_tweets.return_value = Mock(data=mock_tweets)

        result = twitter_client.search_tweets("crypto")

        assert len(result) == 2
        mock_tweepy_api.search_recent_tweets.assert_called_once()
