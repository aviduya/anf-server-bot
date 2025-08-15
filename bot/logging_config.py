from datetime import date
import logging
import os

def setup_logging():
    os.makedirs('./logs', exist_ok=True)

    logging.addLevelName(25, 'USAGE')

    def usage(self, message, *args, **kwargs):
        if self.isEnabledFor(25):
            self._log(25, message, args, **kwargs)

    logging.Logger.usage = usage

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('./logs/bot.log'),
            logging.StreamHandler()
        ]
    )

    logging.info("Logging setup complete")
