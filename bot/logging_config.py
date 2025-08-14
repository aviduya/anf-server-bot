import logging
import os

def setup_logging():
    # Create logs directory
    os.makedirs('logs', exist_ok=True)

    # Add custom USAGE level
    logging.addLevelName(25, 'USAGE')  # Between INFO (20) and WARNING (30)

    def usage(self, message, *args, **kwargs):
        if self.isEnabledFor(25):
            self._log(25, message, args, **kwargs)

    logging.Logger.usage = usage

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/bot.log'),
            logging.StreamHandler()
        ]
    )

    logging.info("Logging setup complete")
