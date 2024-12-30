async def start(update, context):
    user_first_name = update.effective_user.first_name
    await update.message.reply_text(
        f"Привет, {user_first_name}! Я бот, готовый работать круглосуточно. Чем могу помочь?"
    )
