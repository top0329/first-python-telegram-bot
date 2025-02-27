import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler

logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  level=logging.INFO
)

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
  text_caps = ' '.join(context.args).upper()
  await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

if __name__ == '__main__':
  application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

  start_handler = CommandHandler('start', start)
  echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
  caps_handler = CommandHandler('caps', caps)

  application.add_handler(start_handler)
  application.add_handler(echo_handler)
  application.add_handler(caps_handler)

  application.run_polling()
