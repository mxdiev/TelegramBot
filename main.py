from modules.TelegramBot import *
from modules.config import *
from modules.CurrencyConverter import *
from modules.CurrencyRates import *
from modules.SupportedCurrencies import *
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import requests

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    bot = TelegramBot()
    bot.run()
