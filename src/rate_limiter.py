import time
from collections import deque
from typing import Deque
from .config import config as Config
from .logger import get_logger

logger = get_logger()


class RateLimiter:
    def __init__(self) -> None:
        self.requests: Deque[float] = deque()
        self.limit = Config.RATE_LIMIT_PER_MINUTE

    def can_request(self) -> bool:
        now = time.time()
        # Remove old requests
        while self.requests and now - self.requests[0] > 60:
            self.requests.popleft()
        if len(self.requests) < self.limit:
            self.requests.append(now)
            return True
        else:
            logger.warning("Rate limit exceeded")
            return False
