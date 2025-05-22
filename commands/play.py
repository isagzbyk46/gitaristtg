from telegram import Update
from telegram.ext import CallbackContext

def play(update: Update, context: CallbackContext) -> None:
    query = ' '.join(context.args)
    if not query:
        update.message.reply_text('Lütfen bir şarkı adı girin.')
        return

    update.message.reply_text(f'İstediğiniz şarkı: {query}')
