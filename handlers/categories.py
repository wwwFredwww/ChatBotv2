from utils.constants import CATEGORIES

# async def categories(update, context):
#     categories_list = "\n".join([f"• {cat}" for cat in CATEGORIES])
#     message = (
#         "👋 *Доступные категории новостей:*\n"
#         f"{categories_list}\n\n"
#         "Выберите категорию и используйте команду /news <категория>."
#     )
#     await update.message.reply_text(message, parse_mode="Markdown")



#
async def categories(update, context):
    categories_message = "Доступные категории:\n" + "\n".join(f"🔹 {category}" for category in CATEGORIES)
    await update.message.reply_text(categories_message)
