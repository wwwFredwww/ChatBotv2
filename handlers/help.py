from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "👋 *Список доступных команд:*\n"
        "/start - Начать общение с ботом\n"
        "/news <категория> <язык> - Получить новости по категории и языку (пример: /news technology en)\n"
        "/categories - Просмотреть доступные категории новостей\n"
        "/languages - Просмотреть доступные языки перевода\n"
        "/help - Показать это сообщение"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")
