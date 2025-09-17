from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .engagement import EngagementBot
from .logger import get_logger

logger = get_logger()


class Scheduler:
    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler()
        self.bot = EngagementBot()

    def start(self) -> None:
        self.scheduler.add_job(self.bot.post_market_update, "interval", minutes=30)
        self.scheduler.add_job(self.bot.engage_with_tweets, "interval", minutes=15)
        self.scheduler.add_job(self.bot.promote_community, "interval", minutes=60)
        self.scheduler.start()
        logger.info("Scheduler started")

    def stop(self) -> None:
        self.scheduler.shutdown()
        logger.info("Scheduler stopped")
