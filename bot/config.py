import json

from os import getenv

token = getenv("TOKEN")
logs_path = getenv("LOGS_PATH")

with open("./src/messages/chat_messages.json", "r") as file:
    user_messages = json.load(file)

db_connect_data = {
    "drivername": "postgresql",
    "host": getenv("POSTGRES_HOST"),
    "port": getenv("POSTGRES_PORT"),
    "username": getenv("POSTGRES_USER"),
    "password": getenv("POSTGRES_PASSWORD"),
    "database": getenv("POSTGRES_DB"),
}
