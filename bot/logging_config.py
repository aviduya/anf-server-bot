import logging
import os
from logging.handlers import TimedRotatingFileHandler

USAGE = 25
logging.addLevelName(USAGE, "USAGE")

def usage(self, msg, *args, **kwargs):
    if self.isEnabledFor(USAGE):
        self._log(USAGE, msg, args, **kwargs)

logging.Logger.usage = usage

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
