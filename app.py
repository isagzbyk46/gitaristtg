import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from commands.start import start
from commands.play import play

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Ortam değişkenlerini al
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Telegram bot tokeninizi ayarlayın
updater = Updater(token=BOT_TOKEN, use_context=True)

# Komutları kaydet
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('play', play))

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
