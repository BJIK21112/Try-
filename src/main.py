import asyncio
from fastapi import FastAPI, Response
from .scheduler import Scheduler
from .logger import get_logger
from .bot_status import last_market_update, last_engagement, last_promotion
from prometheus_client import generate_latest

app = FastAPI()
logger = get_logger()


@app.on_event("startup")
async def startup_event() -> None:
    scheduler = Scheduler()
    scheduler.start()
    logger.info("Scheduler started")


@app.get("/")
async def root() -> dict:
    return {"message": "X Bot is running"}


@app.get("/status")
async def status() -> dict:
    return {
        "status": "running",
        "last_market_update": last_market_update.isoformat()
        if last_market_update
        else None,
        "last_engagement": last_engagement.isoformat() if last_engagement else None,
        "last_promotion": last_promotion.isoformat() if last_promotion else None,
    }


@app.get("/metrics")
async def metrics() -> Response:
    return Response(content=generate_latest(), media_type="text/plain")


@app.get("/health")
async def health() -> dict:
    return {"status": "healthy"}


@app.post("/trigger-promotion")
async def trigger_promotion() -> dict:
    """Manually trigger a community promotion post for testing"""
    try:
        from .engagement import EngagementBot

        bot = EngagementBot()
        success = bot.promote_community()
        return {
            "status": "success" if success else "failed",
            "message": "Manual promotion triggered",
        }
    except Exception as e:
        logger.error(f"Failed to trigger manual promotion: {e}")
        return {"status": "error", "message": str(e)}


@app.post("/test-post")
async def test_post() -> dict:
    """Post a simple test message to make the account visible"""
    try:
        from .twitter_client import TwitterClient
        from .rate_limiter import RateLimiter
        from .metrics import posts_counter, engagements_counter

        client = TwitterClient()
        limiter = RateLimiter()

        if not limiter.can_request():
            return {
                "status": "rate_limited",
                "message": "Rate limit exceeded, try again later",
            }

        test_message = "🐕 $wifDOG Community Bot is now active! Join the heavenly revolution! 🌟 #wifDOG #memecoin"
        tweet_id = client.post_tweet(test_message)

        if tweet_id:
            posts_counter.inc()
            engagements_counter.inc()
            return {
                "status": "success",
                "message": f"Test post successful! Tweet ID: {tweet_id}",
                "url": f"https://x.com/bishalkunw8/status/{tweet_id}",
            }
        else:
            return {"status": "failed", "message": "Failed to post test message"}
    except Exception as e:
        logger.error(f"Failed to post test message: {e}")
        return {"status": "error", "message": str(e)}


async def main() -> None:
    # For local running
    scheduler = Scheduler()
    scheduler.start()
    try:
        await asyncio.sleep(float("inf"))  # Run forever
    except KeyboardInterrupt:
        scheduler.stop()


if __name__ == "__main__":
    asyncio.run(main())
