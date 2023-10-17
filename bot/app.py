
import src.logger_config

from loguru import logger

from src.telegram_api import app
from modules.errors_module import error_callback
from modules import chat


if __name__ == "__main__":
    logger.info("Inializing complete, bot starting")
    app.add_error_handler(error_callback)
    app.add_handler(chat.weather_handler)
    app.add_handler(chat.photo_handler)
    app.add_handler(chat.file_handler)
    app.add_handler(chat.drink_handler)
    app.run_polling()
