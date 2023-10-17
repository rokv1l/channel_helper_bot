from PIL import Image
import python_weather
from python_weather import Locale
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, MessageHandler, filters, ConversationHandler


async def weather_callback(update: Update, context: CallbackContext):
    async with python_weather.Client(
        unit=python_weather.IMPERIAL, locale=Locale.RUSSIAN
    ) as client:
        weather = await client.get("Moscow")
        text = str((weather.current.temperature - 32) / 1.8) + "C\n"
        text += weather.current.description + "\n"
        await update.effective_chat.send_message(text)


async def file_callback(update: Update, context: CallbackContext):
    await update.effective_chat.send_message("Сохранил на корпоративное хранилище")


async def photo_callback(update: Update, context: CallbackContext):
    file = await update.message.effective_attachment[-1].get_file()
    await file.download_to_drive("tmp.png")
    image = Image.open("tmp.png")
    # maxsize = (1028, 1028)
    rotated_image = image.rotate(180, expand=True)
    rotated_image.save("rotated_tmp.png")
    with open("rotated_tmp.png", "rb") as f:
        await update.effective_chat.send_photo(f)


async def drink_callback(update: Update, callback: CallbackContext):
    await update.effective_chat.send_message(
        'Пришлите мне свои геолокации, и когда все отправят их напишите "Место"'
    )
    return 1


async def loc_callback(update: Update, callback: CallbackContext):
    await update.effective_chat.send_message("Принято")


async def place_callback(update: Update, callback: CallbackContext):
    await update.effective_chat.send_message("Оптимальное место для встречи тут")
    await update.effective_chat.send_location(51.137278, 71.402797)
    return ConversationHandler.END


weather_handler = MessageHandler(filters.Regex("погода|Погода"), weather_callback)
photo_handler = MessageHandler(filters.PHOTO, photo_callback)
file_handler = MessageHandler(filters.Document.ALL, file_callback)
drink_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("Бухать|бухать"), drink_callback)],
    states={
        1: [
            MessageHandler(filters.Regex("Место|место"), place_callback),
            MessageHandler(filters.LOCATION, loc_callback),
        ]
    },
    fallbacks=[],
)
