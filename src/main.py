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
