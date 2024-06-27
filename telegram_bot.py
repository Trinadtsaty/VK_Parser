from Config import tokens
from telegram.ext import Updater, CommandHandler

TOKEN = tokens['telegram_token']


# Индивидуальные идентификаторы чатов для пользователей
# Попросите у пользователей их chat_id и добавьте их сюда
CHAT_IDS = {
    'user1': 'CHAT_ID_1',
    'user2': 'CHAT_ID_2'
}

def start(update, context):
    update.message.reply_text('Привет! Используйте команду /send <user> <message> для отправки сообщения.')

def send_message(update, context):
    if len(context.args) < 2:
        update.message.reply_text('Использование: /send <user> <message>')
        return
    
    user = context.args[0]
    message = ' '.join(context.args[1:])
    
    if user in CHAT_IDS:
        chat_id = CHAT_IDS[user]
        context.bot.send_message(chat_id=chat_id, text=message)
        update.message.reply_text(f'Сообщение отправлено {user}.')
    else:
        update.message.reply_text(f'Пользователь {user} не найден.')

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("send", send_message))

    updater.start_polling()
    updater.idle()

