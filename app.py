import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from pymongo import MongoClient

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Ortam değişkenlerini al
API_HASH = os.getenv("API_HASH")
API_ID = os.getenv("API_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")
HEROKU_API_KEY = os.getenv("HEROKU_API_KEY")
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")
LOGGER_ID = os.getenv("LOGGER_ID")
MONGO_DB_URI = os.getenv("MONGO_DB_URI")
OWNER_ID = os.getenv("OWNER_ID")
STRING_SESSION = os.getenv("STRING_SESSION")

# MongoDB bağlantısı
client = MongoClient(MONGO_DB_URI)
db = client['your_database_name']  # Veritabanı ismini buraya yazın
collection = db['your_collection_name']  # Koleksiyon ismini buraya yazın

# Telegram bot tokeninizi ayarlayın
updater = Updater(token=BOT_TOKEN, use_context=True)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Merhaba! Bot çalışıyor!')
    logger.info(f"Start komutu gönderildi: {update.message.from_user.username}")

def play(update: Update, context: CallbackContext) -> None:
    query = ' '.join(context.args)
    if not query:
        update.message.reply_text('Lütfen bir şarkı adı girin.')
        logger.warning("Şarkı adı verilmedi.")
        return

    # MongoDB'ye kaydetme örneği
    collection.insert_one({"query": query})
    update.message.reply_text(f'İstediğiniz şarkı: {query}')
    logger.info(f"Şarkı istendi: {query}")

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def respond():
    update = Update.de_json(request.get_json(force=True))
    updater.dispatcher.process_update(update)
    return 'ok'

@app.route('/')
def index():
    return 'Telegram botu çalışıyor!'

if __name__ == '__main__':
    app.run(debug=True)
