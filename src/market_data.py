import requests
from typing import List, Optional
from .config import config as Config
from .logger import get_logger

logger = get_logger()


class MarketData:
    BASE_URL = "https://api.coingecko.com/api/v3"

    def get_trending_coins(self) -> List[str]:
        url = f"{self.BASE_URL}/search/trending"
        headers = {"accept": "application/json"}
        if Config.COINGECKO_API_KEY:
            headers["x-cg-demo-api-key"] = Config.COINGECKO_API_KEY
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            coins = [coin["item"]["id"] for coin in data["coins"]]
            logger.info(f"Trending coins: {coins}")
            return coins
        except Exception as e:
            logger.error(f"Error fetching trending coins: {e}")
            return []

    def get_coin_price(self, coin_id: str) -> Optional[float]:
        url = f"{self.BASE_URL}/simple/price?ids={coin_id}&vs_currencies=usd"
        headers = {"accept": "application/json"}
        if Config.COINGECKO_API_KEY:
            headers["x-cg-demo-api-key"] = Config.COINGECKO_API_KEY
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            price = data.get(coin_id, {}).get("usd")
            logger.info(f"Price of {coin_id}: {price}")
            return float(price) if price is not None else None
        except Exception as e:
            logger.error(f"Error fetching price for {coin_id}: {e}")
            return None
