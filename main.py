import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, InlineQueryHandler
from uuid import uuid4

logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  level=logging.INFO
)

logger = logging.getLogger(__name__)

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
  text_caps = ' '.join(context.args).upper()
  await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.inline_query.query
  logger.info(f"Received inline query: {query}")
  if not query:
    logger.info("Empty query received, returning")
    return
  results = []
  results.append(
    InlineQueryResultArticle(
      id=str(uuid4()),
      title='Caps',
      input_message_content=InputTextMessageContent(query.upper())
    )
  )
  logger.info(f"Sending capitalized result: {query.upper()}")
  await context.bot.answer_inline_query(update.inline_query.id, results)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

if __name__ == '__main__':
  application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

  start_handler = CommandHandler('start', start)
  echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
  caps_handler = CommandHandler('caps', caps)
  inline_caps_handler = InlineQueryHandler(inline_caps)
  unknown_handler = MessageHandler(filters.COMMAND, unknown)

  application.add_handler(start_handler)
  application.add_handler(echo_handler)
  application.add_handler(caps_handler)
  application.add_handler(inline_caps_handler)
  application.add_handler(unknown_handler)

  application.run_polling()
