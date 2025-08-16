import logging
import os
from logging.handlers import TimedRotatingFileHandler
import functools

USAGE = 25
logging.addLevelName(USAGE, "USAGE")

def _usage(self, msg, *args, **kwargs):
    if self.isEnabledFor(USAGE):
        self._log(USAGE, msg, args, **kwargs)

logging.Logger.usage = _usage

def setup_logging():
    os.makedirs("./logs", exist_ok=True)
    handler = TimedRotatingFileHandler(
        "./logs/bot.log", when="midnight", backupCount=7, encoding="utf-8"
    )
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[handler, logging.StreamHandler()]
    )
    return logging.getLogger("bot")

log = logging.getLogger("bot")

def log_usage(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        interaction = kwargs.get("interaction")
        if interaction is None:
            for a in args:
                if getattr(a, "user", None) is not None:
                    interaction = a
                    break

        user = getattr(getattr(interaction, "user", None), "name", None) or "unknown-user"
        log.usage(f"{user} invoked {func.__name__}")
        try:
            result = await func(*args, **kwargs)
            log.usage(f"{func.__name__} completed for {user}")
            return result
        except Exception as e:
            log.error(f"{func.__name__} failed for {user}: {e}", exc_info=True)
            raise
    return wrapper
