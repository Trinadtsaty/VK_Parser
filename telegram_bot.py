from Config import tokens
# TOKEN = tokens['telegram_token']
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging




# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()

# Обработчик команды /send
async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE, message= "разараб еблан, не передал massage"):
    # if context.args:
        await update.message.reply_text(message)
    # else:
    #     await update.message.reply_text("Пожалуйста, предоставьте сообщение для отправки.")

def run_tg_bot():
    # Вставьте ваш токен бота здесь
    token = tokens['telegram_token']
    # Создание экземпляра приложения
    application = ApplicationBuilder().token(token).build()
    
    # Добавление обработчика команды /send
    application.add_handler(CommandHandler('send', send_message))

    # Запуск polling
    logger.info("Запуск бота...")
    application.run_polling()


run_tg_bot()
