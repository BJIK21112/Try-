import tweepy
from typing import Optional, List, Any
from .config import config as Config
from .logger import get_logger

logger = get_logger()


class TwitterClient:
    def __init__(self) -> None:
        self.client = tweepy.Client(
            bearer_token=Config.TWITTER_BEARER_TOKEN,
            consumer_key=Config.TWITTER_CLIENT_ID,
            consumer_secret=Config.TWITTER_CLIENT_SECRET,
            access_token=Config.TWITTER_ACCESS_TOKEN,
            access_token_secret=Config.TWITTER_ACCESS_TOKEN_SECRET,
        )

    def post_tweet(self, text: str) -> Optional[str]:
        try:
            response = self.client.create_tweet(text=text)
            logger.info(f"Posted tweet: {response.data['id']}")
            return str(response.data["id"])
        except Exception as e:
            logger.error(f"Error posting tweet: {e}")
            return None

    def reply_to_tweet(self, tweet_id: str, text: str) -> Optional[str]:
        try:
            response = self.client.create_tweet(
                text=text, in_reply_to_tweet_id=tweet_id
            )
            logger.info(f"Replied to tweet {tweet_id}: {response.data['id']}")
            return str(response.data["id"])
        except Exception as e:
            logger.error(f"Error replying to tweet: {e}")
            return None

    def like_tweet(self, tweet_id: str) -> None:
        try:
            self.client.like(tweet_id)
            logger.info(f"Liked tweet: {tweet_id}")
        except Exception as e:
            logger.error(f"Error liking tweet: {e}")

    def retweet(self, tweet_id: str) -> None:
        try:
            self.client.retweet(tweet_id)
            logger.info(f"Retweeted tweet: {tweet_id}")
        except Exception as e:
            logger.error(f"Error retweeting tweet: {e}")

    def search_tweets(self, query: str, max_results: int = 10) -> List[Any]:
        try:
            tweets = self.client.search_recent_tweets(
                query=query, max_results=max_results
            )
            return list(tweets.data) if tweets.data else []
        except Exception as e:
            logger.error(f"Error searching tweets: {e}")
            return []
