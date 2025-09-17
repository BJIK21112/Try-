from .twitter_client import TwitterClient
from .market_data import MarketData
from .rate_limiter import RateLimiter
from .spam_detector import SpamDetector
from .logger import get_logger
from .metrics import posts_counter, likes_counter, replies_counter, engagements_counter
from . import bot_status
from datetime import datetime

logger = get_logger()


class EngagementBot:
    def __init__(self) -> None:
        self.twitter = TwitterClient()
        self.market = MarketData()
        self.rate_limiter = RateLimiter()
        self.spam_detector = SpamDetector()

    def post_market_update(self) -> None:
        if not self.rate_limiter.can_request():
            logger.warning(
                "Rate limit exceeded for market update",
                extra={"action": "market_update", "rate_limited": True},
            )
            return
        trending = self.market.get_trending_coins()
        if trending:
            coin = trending[0]
            price = self.market.get_coin_price(coin)
            if price:
                text = (
                    f"Trending memecoin: {coin.capitalize()} at ${price} USD. "
                    "#memecoin #crypto"
                )
                tweet_id = self.twitter.post_tweet(text)
                if tweet_id:
                    posts_counter.inc()
                    engagements_counter.inc()
                    logger.info(
                        "Market update posted successfully",
                        extra={
                            "action": "market_update",
                            "coin": coin,
                            "price": price,
                            "tweet_id": tweet_id,
                            "success": True,
                        },
                    )
                else:
                    logger.error(
                        "Failed to post market update",
                        extra={
                            "action": "market_update",
                            "coin": coin,
                            "price": price,
                            "success": False,
                        },
                    )
            else:
                logger.warning(
                    "Could not fetch price for trending coin",
                    extra={
                        "action": "market_update",
                        "coin": coin,
                        "price_fetched": False,
                    },
                )
        else:
            logger.warning(
                "No trending coins available",
                extra={"action": "market_update", "trending_available": False},
            )
        bot_status.last_market_update = datetime.now()

    def engage_with_tweets(
        self,
        query: str = 'wifDOG OR solwifDOG OR wifDOG OR memecoin OR crypto OR kukur OR tihar OR "dog festival" OR nepal',
    ) -> None:
        logger.info(
            "Starting tweet engagement",
            extra={"action": "engage_tweets", "query": query},
        )
        tweets = self.twitter.search_tweets(query)
        engaged_count = 0
        for tweet in tweets:
            if self.spam_detector.is_spam(tweet.text):
                logger.info(
                    "Skipped spam tweet",
                    extra={
                        "action": "engage_tweets",
                        "tweet_id": tweet.id,
                        "reason": "spam",
                    },
                )
                continue
            if not self.rate_limiter.can_request():
                logger.warning(
                    "Rate limit reached during engagement",
                    extra={"action": "engage_tweets", "engaged_count": engaged_count},
                )
                break
            # Simple engagement: like and reply
            self.twitter.like_tweet(tweet.id)
            likes_counter.inc()
            engagements_counter.inc()
            reply_text = "Fascinating cultural insight! Dogs hold a special place in many cultures. 🐕 #KukurTihar #CulturalHeritage"
            tweet_id = self.twitter.reply_to_tweet(tweet.id, reply_text)
            if tweet_id:
                replies_counter.inc()
                engagements_counter.inc()
                logger.info(
                    "Successfully engaged with tweet",
                    extra={
                        "action": "engage_tweets",
                        "original_tweet_id": tweet.id,
                        "reply_tweet_id": tweet_id,
                        "engagement_type": "like_and_reply",
                    },
                )
                engaged_count += 1
            else:
                logger.warning(
                    "Failed to reply to tweet",
                    extra={
                        "action": "engage_tweets",
                        "tweet_id": tweet.id,
                        "engagement_type": "like_only",
                    },
                )
        logger.info(
            "Tweet engagement completed",
            extra={"action": "engage_tweets", "total_engaged": engaged_count},
        )
        bot_status.last_engagement = datetime.now()

    def promote_community(self) -> None:
        if not self.rate_limiter.can_request():
            logger.warning(
                "Rate limit exceeded for community promotion",
                extra={"action": "promote_community", "rate_limited": True},
            )
            return

        # Enhanced $wifDOG promotion messages with trending elements
        promotion_messages = [
            "🚀 $wifDOG is taking over! Join the heavenly revolution in crypto! 🌟 https://x.com/i/communities/1968070058237890732 #wifDOG #memecoin #crypto #Solana",
            "🐕 Divine $wifDOG community growing fast! Don't miss this celestial opportunity! ⭐ https://x.com/i/communities/1968070058237890732 #wifDOG #altcoins #trading",
            "🌙 $wifDOG: Where dogs meet divinity in the crypto space! Join now! 🐕‍🦺 https://x.com/i/communities/1968070058237890732 #wifDOG #DeFi #NFT",
            "🔥 $wifDOG trending! Heavenly gains await in this dog-themed revolution! 🌟 https://x.com/i/communities/1968070058237890732 #wifDOG #crypto #blockchain",
            "✨ Discover $wifDOG - the ultimate crypto companion for your portfolio! 🐕 https://x.com/i/communities/1968070058237890732 #wifDOG #investing #memecoins",
        ]

        # Rotate through different messages
        import random

        text = random.choice(promotion_messages)

        tweet_id = self.twitter.post_tweet(text)
        if tweet_id:
            posts_counter.inc()
            engagements_counter.inc()
            logger.info(
                "Community promotion posted successfully",
                extra={
                    "action": "promote_community",
                    "tweet_id": tweet_id,
                    "success": True,
                },
            )
        else:
            logger.error(
                "Failed to post community promotion",
                extra={"action": "promote_community", "success": False},
            )
        bot_status.last_promotion = datetime.now()

    def promote_specific_post(self) -> None:
        """Promote the specific $wifDOG post with groundbreaking SEO and trending elements"""
        if not self.rate_limiter.can_request():
            logger.warning(
                "Rate limit exceeded for specific post promotion",
                extra={"action": "promote_specific_post", "rate_limited": True},
            )
            return

        target_tweet_id = "1968073148789821487"  # The specific post to promote

        # Enhanced promotion messages for the specific post
        promotion_messages = [
            "🚀 This $wifDOG breakdown is pure gold! Essential reading for crypto enthusiasts! 📈 https://x.com/AadityaDhu71908/status/1968073148789821487 #wifDOG #crypto #memecoin #Solana #trading",
            "🔥 Mind-blowing $wifDOG analysis! This post explains everything you need to know! 🌟 https://x.com/AadityaDhu71908/status/1968073148789821487 #wifDOG #blockchain #DeFi #NFT #investing",
            "💎 $wifDOG community favorite! This thread is a game-changer for the space! 🐕 https://x.com/AadityaDhu71908/status/1968073148789821487 #wifDOG #altcoins #cryptocurrency #memecoins",
            "⚡ Revolutionary $wifDOG insights! Don't sleep on this comprehensive breakdown! 🌙 https://x.com/AadityaDhu71908/status/1968073148789821487 #wifDOG #cryptoanalysis #trading #blockchain",
            "🌟 $wifDOG phenomenon explained! This post captures the essence perfectly! ✨ https://x.com/AadityaDhu71908/status/1968073148789821487 #wifDOG #memecoin #Solana #cryptocommunity",
        ]

        import random

        promotion_text = random.choice(promotion_messages)

        # Try to reply to the specific post
        reply_id = self.twitter.reply_to_tweet(target_tweet_id, promotion_text)
        if reply_id:
            replies_counter.inc()
            engagements_counter.inc()
            logger.info(
                "Specific post promotion successful",
                extra={
                    "action": "promote_specific_post",
                    "target_tweet_id": target_tweet_id,
                    "reply_id": reply_id,
                    "success": True,
                },
            )
        else:
            # If reply fails, try posting a standalone promotion
            standalone_text = "🔥 Must-read $wifDOG analysis! Complete breakdown here: https://x.com/AadityaDhu71908/status/1968073148789821487 #wifDOG #crypto #memecoin #Solana"
            tweet_id = self.twitter.post_tweet(standalone_text)
            if tweet_id:
                posts_counter.inc()
                engagements_counter.inc()
                logger.info(
                    "Specific post promotion (standalone) successful",
                    extra={
                        "action": "promote_specific_post",
                        "target_tweet_id": target_tweet_id,
                        "tweet_id": tweet_id,
                        "success": True,
                    },
                )
            else:
                logger.error(
                    "Failed to promote specific post",
                    extra={
                        "action": "promote_specific_post",
                        "target_tweet_id": target_tweet_id,
                        "success": False,
                    },
                )

        bot_status.last_specific_promotion = datetime.now()
