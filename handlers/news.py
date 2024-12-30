from services.news_service import get_latest_news
from services.translator import translate_text
from utils.constants import CATEGORIES

async def news(update, context):
    args = context.args
    category = args[0] if len(args) > 0 else "technology"
    language = args[1] if len(args) > 1 else "ru"

    if category not in CATEGORIES:
        await update.message.reply_text(
            "❌ Неверная категория. Используйте команду /categories для просмотра доступных категорий."
        )
        return

    news_list = get_latest_news(category)
    if not news_list:
        await update.message.reply_text("❌ Новости не найдены. Попробуйте позже.")
        return

    for news_item in news_list:
        translated_title = translate_text(news_item["title"], dest_language=language)
        message_text = (
            f"📰 *{translated_title}*\n\n"
            f"🔗 [Читать подробнее]({news_item['url']})"
        )
        if news_item["image"]:
            await update.message.reply_photo(news_item["image"], caption=message_text, parse_mode="Markdown")
        else:
            await update.message.reply_text(message_text, parse_mode="Markdown")
