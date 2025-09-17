from .config import config as Config
from .logger import get_logger

logger = get_logger()


class SpamDetector:
    SPAM_KEYWORDS = ["spam", "scam", "fake", "pump", "dump"]

    def is_spam(self, text: str) -> bool:
        text_lower = text.lower()
        spam_count = sum(1 for word in self.SPAM_KEYWORDS if word in text_lower)
        if spam_count >= Config.SPAM_THRESHOLD:
            logger.warning(f"Detected spam: {text}")
            return True
        return False
