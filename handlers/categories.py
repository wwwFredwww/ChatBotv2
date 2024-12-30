from utils.constants import CATEGORIES

async def categories(update, context):
    categories_message = "Доступные категории:\n" + "\n".join(f"🔹 {category}" for category in CATEGORIES)
    await update.message.reply_text(categories_message)
