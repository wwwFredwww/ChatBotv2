from telegram.ext import ApplicationBuilder, CommandHandler
from backgraund import keep_alive  # Flask для "оживления" бота
import requests
from deep_translator import GoogleTranslator

# Токен вашего бота
TOKEN = "7989705777:AAGb22SDfZHktTREPPwXGcpskQHkMcNiw-g"

# Функция для обработки команды /start
async def start(update, context):
    user_first_name = update.effective_user.first_name
    await update.message.reply_text(
        f"Привет, {user_first_name}! Я бот, готовый работать круглосуточно. Чем могу помочь?"
    )

# Функция для обработки команды /languages
async def languages(update, context):
    available_languages = {"ru": "Русский", "en": "English", "es": "Español", "de": "Deutsch"}
    language_list = "\n".join(f"{code}: {name}" for code, name in available_languages.items())
    await update.message.reply_text(f"Доступные языки перевода:\n\n{language_list}")

# Функция для обработки команды /categories
async def categories(update, context):
    categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]
    categories_message = "Доступные категории:\n" + "\n".join(f"🔹 {category}" for category in categories)
    await update.message.reply_text(categories_message)

# Функция для перевода текста
def translate_text(text, dest_language="ru"):
    try:
        # Используем GoogleTranslator из deep-translator
        translated = GoogleTranslator(source='auto', target=dest_language).translate(text)
        return translated
    except Exception as e:
        print(f"Ошибка перевода: {e}")
        return "❌ Перевод временно недоступен."

# Функция для получения последних новостей
def get_latest_news(category="technology"):
    try:
        api_key = "5c576dc45ba04d9d9667093c7329705b"
        url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("status") != "ok":
            print(f"Ошибка API: {data.get('message')}")
            return None
        return [article["title"] for article in data.get("articles", [])[:5]]
    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения: {e}")
        return None
    except Exception as e:
        print(f"Общая ошибка: {e}")
        return None

# Функция для обработки команды /news
async def news(update, context):
    args = context.args

    # Проверяем количество аргументов
    if len(args) > 2:
        await update.message.reply_text("❌ Слишком много аргументов. Формат: /news <категория> <язык>.")
        return

    # Получаем категорию и язык
    category = args[0] if len(args) > 0 else "technology"
    language = args[1] if len(args) > 1 else "ru"

    # Проверяем валидность категории
    valid_categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]
    if category not in valid_categories:
        await update.message.reply_text(
            "❌ Неверная категория. Используйте команду /categories для просмотра доступных категорий."
        )
        return

    # Получаем новости
    news_list = get_latest_news(category)
    if not news_list:
        await update.message.reply_text("❌ Новости не найдены. Попробуйте позже.")
        return

    # Переводим и отправляем новости
    try:
        translated_news = [translate_text(news, dest_language=language) for news in news_list]
        news_message = (
            f"📰 *Последние новости на {language.upper()} (категория: {category}):*\n\n"
            + "\n\n".join(f"🔹 {news}" for news in translated_news)
        )
        await update.message.reply_text(news_message, parse_mode="Markdown")
    except Exception as e:
        print(f"Ошибка обработки новостей: {e}")
        await update.message.reply_text("❌ Произошла ошибка при обработке новостей. Попробуйте позже.")

# Функция для обработки команды /help
async def help_command(update, context):
    help_text = (
        "👋 *Список доступных команд:*\n"
        "/start - Начать общение с ботом\n"
        "/news <категория> <язык> - Получить новости по категории и языку (пример: /news technology en)\n"
        "/categories - Просмотреть доступные категории новостей\n"
        "/languages - Просмотреть доступные языки перевода\n"
        "/help - Показать это сообщение"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

# Основная функция запуска бота
def main():
    # Создаем приложение Telegram
    telegram_app = ApplicationBuilder().token(TOKEN).build()

    # Добавляем обработчики команд
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("languages", languages))
    telegram_app.add_handler(CommandHandler("categories", categories))
    telegram_app.add_handler(CommandHandler("news", news))  # Команда /news
    telegram_app.add_handler(CommandHandler("help", help_command))

    # Запускаем Flask для предотвращения "засыпания" приложения
    keep_alive()

    # Запускаем бот в режиме polling
    telegram_app.run_polling()

if __name__ == "__main__":
    main()

