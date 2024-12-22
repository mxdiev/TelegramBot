from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import requests
from modules.config import *

class TelegramBot:
    def __init__(self):
        self.application = Application.builder().token(BOT_TOKEN).build()
        self._add_handlers()

    def _add_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help))
        self.application.add_handler(CommandHandler("convert", self.convert))
        self.application.add_handler(CommandHandler("currencies", self.currencies))
        self.application.add_handler(CommandHandler("rates", self.rates))
        self.application.add_handler(CallbackQueryHandler(self.handle_buttons))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.unknown_command))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        keyboard = [
            [InlineKeyboardButton("Конвертировать валюту", callback_data="convert")],
            [InlineKeyboardButton("Список валют", callback_data="currencies")],
            [InlineKeyboardButton("Курсы валют", callback_data="rates")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"Привет, {user.first_name}!\n"
            f"Добро пожаловать в Финансового Бота!\n"
            f"С помощью этого бота вы можете узнавать обменные курсы валют.",
            reply_markup=reply_markup
        )

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Доступные команды:\n"
            "/convert [сумма] [базовая_валюта] [целевая_валюта] - Конвертировать сумму из одной валюты в другую\n"
            "/currencies - Показать список всех поддерживаемых валют\n"
            "/rates [базовая_валюта] - Показать курсы валют относительно базовой валюты\n"
            "Пример: /convert 100 USD EUR или /rates USD"
        )

    async def handle_buttons(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        if query.data == "convert":
            await query.message.reply_text(
                "Для конвертации используйте команду: /convert [сумма] [базовая_валюта] [целевая_валюта]"
            )
        elif query.data == "currencies":
            await self.currencies(query, context)
        elif query.data == "rates":
            await query.message.reply_text(
                "Для получения курсов используйте команду: /rates [базовая_валюта]"
            )

    async def convert(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if len(context.args) < 3:
            await update.message.reply_text("Использование: /convert [сумма] [базовая_валюта] [целевая_валюта]")
            return

        try:
            amount = float(context.args[0])
            base_currency = context.args[1].upper()
            target_currency = context.args[2].upper()

            result = CurrencyConverter.convert(amount, base_currency, target_currency)
            if result:
                await update.message.reply_text(f"{amount} {base_currency} = {result:.2f} {target_currency}")
            else:
                await update.message.reply_text("Неверные валюты или данные недоступны. Попробуйте снова.")
        except ValueError:
            await update.message.reply_text("Сумма должна быть числом. Пример: /convert 100 USD EUR")
        except Exception as e:
            logger.error(f"Ошибка в команде /convert: {e}")
            await update.message.reply_text("Произошла ошибка при обработке вашего запроса.")

    async def currencies(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        currencies = SupportedCurrencies.get_supported()
        if currencies:
            currency_list = "\n".join(currencies)
            await update.message.reply_text(f"Поддерживаемые валюты:\n{currency_list}")
        else:
            await update.message.reply_text("Не удалось получить список валют. Попробуйте позже.")

    async def rates(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if len(context.args) < 1:
            await update.message.reply_text("Использование: /rates [базовая_валюта]")
            return

        base_currency = context.args[0].upper()
        rates = CurrencyRates.get_all_rates(base_currency)

        if rates:
            rates_list = "\n".join([f"{currency}: {rate:.2f}" for currency, rate in rates.items()])
            await update.message.reply_text(f"Курсы валют относительно {base_currency}:\n{rates_list}")
        else:
            await update.message.reply_text("Не удалось получить курсы. Попробуйте позже.")

    async def unknown_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Неизвестная команда. Используйте /help, чтобы увидеть список доступных команд."
        )

    def run(self):
        self.application.run_polling()