from utils.constants import AVAILABLE_LANGUAGES

async def languages(update, context):
    language_list = "\n".join(f"{code}: {name}" for code, name in AVAILABLE_LANGUAGES.items())
    await update.message.reply_text(f"Доступные языки перевода:\n\n{language_list}")
