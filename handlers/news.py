import requests
from deep_translator import GoogleTranslator
from utils.constants import CATEGORIES, AVAILABLE_LANGUAGES

async def news(update, context):
    args = context.args
    if len(args) < 2:
        available_langs = ', '.join(f"{key} ({value})" for key, value in AVAILABLE_LANGUAGES.items())
        await update.message.reply_text(
            f"Пожалуйста, укажите категорию и язык перевода. Пример: /news animechan ru\n"
            f"Доступные языки: {available_langs}"
        )
        return

    category = args[0].lower()
    language = args[1].lower()

    # Проверка, что язык указан правильно
    if language not in AVAILABLE_LANGUAGES:
        available_langs = ', '.join(f"{key} ({value})" for key, value in AVAILABLE_LANGUAGES.items())
        await update.message.reply_text(
            f"Неверный язык. Используйте один из следующих: {available_langs}"
        )
        return

    if category not in CATEGORIES:
        await update.message.reply_text(f"Неверная категория. Используйте одну из следующих: {', '.join(CATEGORIES)}")
        return

    if category == "animechan":
        # AnimeChan API запрос
        url = "https://animechan.xyz/api/random"
        response = requests.get(url)

        if response.status_code == 200:
            try:
                data = response.json()
                anime = data.get("anime", "Неизвестное аниме")
                character = data.get("character", "Неизвестный персонаж")
                quote = data.get("quote", "Цитата отсутствует")

                # Перевод цитаты на выбранный язык
                translated_quote = GoogleTranslator(source="en", target=language).translate(quote)

                # Формируем сообщение
                message = (
                    f"🎌 *Цитата из аниме*: _{anime}_\n"
                    f"👤 *Персонаж*: {character}\n"
                    f"💬 *Цитата*: {translated_quote}"
                )

                await update.message.reply_text(message, parse_mode="Markdown")
            except Exception as e:
                await update.message.reply_text(f"Произошла ошибка при обработке данных: {e}")
        else:
            await update.message.reply_text("Не удалось получить цитату. Попробуйте позже.")
    elif category == "jikan_anime":
        # Jikan API запрос
        url = "https://api.jikan.moe/v4/top/anime"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            top_anime = data["data"][:5]  # Топ-5 аниме

            for anime in top_anime:
                title = anime["title"]
                translated_title = GoogleTranslator(source="en", target=language).translate(title)

                score = anime.get("score", "N/A")
                synopsis = anime.get("synopsis", "Описание недоступно")
                translated_synopsis = GoogleTranslator(source="en", target=language).translate(synopsis)

                image_url = anime["images"]["jpg"]["image_url"]
                trailer_url = anime.get("trailer", {}).get("url", "Трейлер недоступен")

                # Формируем текст сообщения
                message = (
                    f"🎥 *{translated_title}* (Рейтинг: {score})\n"
                    f"📖 Описание: {translated_synopsis}\n"
                    f"📺 [Трейлер]({trailer_url})"
                )

                # Проверяем длину текста
                if len(message) > 1024:
                    message_parts = [message[i:i+1024] for i in range(0, len(message), 1024)]
                    await context.bot.send_photo(
                        chat_id=update.effective_chat.id,
                        photo=image_url,
                        caption=message_parts[0],
                        parse_mode="Markdown"
                    )
                    for part in message_parts[1:]:
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=part,
                            parse_mode="Markdown"
                        )
                else:
                    await context.bot.send_photo(
                        chat_id=update.effective_chat.id,
                        photo=image_url,
                        caption=message,
                        parse_mode="Markdown"
                    )
        else:
            await update.message.reply_text("Не удалось получить данные о аниме. Попробуйте позже.")
    else:
        await update.message.reply_text(f"Вы выбрали категорию: {category}. Пока она не поддерживается.")


# ------------------------------------v2------------------------------------
# import requests
# from deep_translator import GoogleTranslator
#
# from utils.constants import CATEGORIES
#
# from utils.constants import AVAILABLE_LANGUAGES
#
# async def news(update, context):
#     args = context.args
#     if len(args) < 1:
#         await update.message.reply_text("Пожалуйста, укажите категорию. Пример: /news technology")
#         return
#
#     category = args[0].lower()
#     if category not in CATEGORIES:
#         await update.message.reply_text(f"Неверная категория. Используйте одну из следующих: {', '.join(CATEGORIES)}")
#         return
#
#     if category == "animechan":
#         # AnimeChan API запрос
#         url = "https://animechan.xyz/api/random"
#         response = requests.get(url)
#
#         if response.status_code == 200:
#             try:
#                 data = response.json()
#                 anime = data.get("anime", "Неизвестное аниме")
#                 character = data.get("character", "Неизвестный персонаж")
#                 quote = data.get("quote", "Цитата отсутствует")
#
#                 # Перевод цитаты на русский
#                 translated_quote = GoogleTranslator(source="en", target="ru").translate(quote)
#
#                 # Формируем сообщение
#                 message = (
#                     f"🎌 *Цитата из аниме*: _{anime}_\n"
#                     f"👤 *Персонаж*: {character}\n"
#                     f"💬 *Цитата*: {translated_quote}"
#                 )
#
#                 await update.message.reply_text(message, parse_mode="Markdown")
#             except Exception as e:
#                 await update.message.reply_text(f"Произошла ошибка при обработке данных: {e}")
#         else:
#             await update.message.reply_text("Не удалось получить цитату. Попробуйте позже.")
#     elif category == "jikan_anime":
#     #  Jikan API запрос
#         url = "https://api.jikan.moe/v4/top/anime"
#         response = requests.get(url)
#
#         if response.status_code == 200:
#             data = response.json()
#             top_anime = data["data"][:5]  # Топ-5 аниме
#
#             for anime in top_anime:
#                 title = anime["title"]  # Название
#                 translated_title = GoogleTranslator(source="en", target="ru").translate(title)
#
#                 score = anime.get("score", "N/A")  # Оценка
#                 synopsis = anime.get("synopsis", "Описание недоступно")  # Описание
#                 translated_synopsis = GoogleTranslator(source="en", target="ru").translate(synopsis)
#
#                 image_url = anime["images"]["jpg"]["image_url"]  # Картинка
#                 trailer_url = anime.get("trailer", {}).get("url", "Трейлер недоступен")  # Трейлер
#
#                 # Формируем текст сообщения
#                 message = (
#                     f"🎥 *{translated_title}* (Рейтинг: {score})\n"
#                     f"📖 Описание: {translated_synopsis}\n"
#                     f"📺 [Трейлер]({trailer_url})"
#                 )
#
#                 # Проверяем длину текста
#                 if len(message) > 1024:
#                     # Если текст слишком длинный, разделяем его на части
#                     message_parts = [
#                         message[i:i+1024] for i in range(0, len(message), 1024)
#                     ]
#                     await context.bot.send_photo(
#                         chat_id=update.effective_chat.id,
#                         photo=image_url,
#                         caption=message_parts[0],  # Первая часть будет подписью
#                         parse_mode="Markdown"
#                     )
#                     # Отправляем остальные части как текстовые сообщения
#                     for part in message_parts[1:]:
#                         await context.bot.send_message(
#                             chat_id=update.effective_chat.id,
#                             text=part,
#                             parse_mode="Markdown"
#                         )
#                 else:
#                     # Если текст помещается в 1024 символа, отправляем его
#                     await context.bot.send_photo(
#                         chat_id=update.effective_chat.id,
#                         photo=image_url,
#                         caption=message,
#                         parse_mode="Markdown"
#                     )
#         else:
#             await update.message.reply_text("Не удалось получить данные о аниме. Попробуйте позже.")
#     else:
#         await update.message.reply_text(f"Вы выбрали категорию: {category}. Пока она не поддерживается.")


# -----------------------------------------------------------------
# async def news(update, context):
#     args = context.args
#     if len(args) < 1:
#         await update.message.reply_text("Пожалуйста, укажите категорию. Пример: /news technology")
#         return
#
#     category = args[0].lower()
#     if category not in CATEGORIES:
#         await update.message.reply_text(f"Неверная категория. Используйте одну из следующих: {', '.join(CATEGORIES)}")
#         return
#
#     if category == "jikan_anime":
#         # Jikan API запрос
#         url = "https://api.jikan.moe/v4/top/anime"
#         response = requests.get(url)
#
#         if response.status_code == 200:
#             data = response.json()
#             top_anime = data["data"][:5]  # Топ-5 аниме
#
#             for anime in top_anime:
#                 title = anime["title"]  # Название
#                 translated_title = GoogleTranslator(source="en", target="ru").translate(title)
#
#                 score = anime.get("score", "N/A")  # Оценка
#                 synopsis = anime.get("synopsis", "Описание недоступно")  # Описание
#                 translated_synopsis = GoogleTranslator(source="en", target="ru").translate(synopsis)
#
#                 image_url = anime["images"]["jpg"]["image_url"]  # Картинка
#                 trailer_url = anime.get("trailer", {}).get("url", "Трейлер недоступен")  # Трейлер
#
#                 # Формируем текст сообщения
#                 message = (
#                     f"🎥 *{translated_title}* (Рейтинг: {score})\n"
#                     f"📖 Описание: {translated_synopsis}\n"
#                     f"📺 [Трейлер]({trailer_url})"
#                 )
#
#                 # Проверяем длину текста
#                 if len(message) > 1024:
#                     # Если текст слишком длинный, разделяем его на части
#                     message_parts = [
#                         message[i:i+1024] for i in range(0, len(message), 1024)
#                     ]
#                     await context.bot.send_photo(
#                         chat_id=update.effective_chat.id,
#                         photo=image_url,
#                         caption=message_parts[0],  # Первая часть будет подписью
#                         parse_mode="Markdown"
#                     )
#                     # Отправляем остальные части как текстовые сообщения
#                     for part in message_parts[1:]:
#                         await context.bot.send_message(
#                             chat_id=update.effective_chat.id,
#                             text=part,
#                             parse_mode="Markdown"
#                         )
#                 else:
#                     # Если текст помещается в 1024 символа, отправляем его
#                     await context.bot.send_photo(
#                         chat_id=update.effective_chat.id,
#                         photo=image_url,
#                         caption=message,
#                         parse_mode="Markdown"
#                     )
#         else:
#             await update.message.reply_text("Не удалось получить данные о аниме. Попробуйте позже.")
#     else:
#         await update.message.reply_text(f"Вы выбрали категорию: {category}. Пока она не поддерживается.")

#_________________________________________________________________________
# import requests
# from utils.constants import CATEGORIES
#
# async def news(update, context):
#     # Получаем параметры из команды
#     args = context.args
#     if len(args) < 1:
#         await update.message.reply_text("Пожалуйста, укажите категорию. Пример: /news technology")
#         return
#
#     category = args[0].lower()
#     if category not in CATEGORIES:
#         await update.message.reply_text(f"Неверная категория. Используйте одну из следующих: {', '.join(CATEGORIES)}")
#         return
#
#     if category == "jikan_anime":
#         # Используем Jikan API для получения данных о популярных аниме
#         url = "https://api.jikan.moe/v4/top/anime"
#         response = requests.get(url)
#
#         if response.status_code == 200:
#             data = response.json()
#             top_anime = data["data"][:5]  # Берём топ-5 аниме
#
#             message = "*Топ аниме:*\n\n"
#             for anime in top_anime:
#                 title = anime["title"]
#                 score = anime.get("score", "N/A")
#                 url = anime["url"]
#                 message += f"🎥 *{title}* (Rating: {score})\n🔗 [Подробнее]({url})\n\n"
#
#             await update.message.reply_text(message, parse_mode="Markdown")
#         else:
#             await update.message.reply_text("Не удалось получить данные о аниме. Попробуйте позже.")
#     else:
#         # Обработка других категорий
#         await update.message.reply_text(f"Вы выбрали категорию: {category}. Пока она не поддерживается.")


# from services.news_service import get_latest_news
# from services.translator import translate_text
# from utils.constants import CATEGORIES
#
# async def news(update, context):
#     args = context.args
#     category = args[0] if len(args) > 0 else "technology"
#     language = args[1] if len(args) > 1 else "ru"
#
#     if category not in CATEGORIES:
#         await update.message.reply_text(
#             "❌ Неверная категория. Используйте команду /categories для просмотра доступных категорий."
#         )
#         return
#
#     news_list = get_latest_news(category)
#     if not news_list:
#         await update.message.reply_text("❌ Новости не найдены. Попробуйте позже.")
#         return
#
#     for news_item in news_list:
#         translated_title = translate_text(news_item["title"], dest_language=language)
#         message_text = (
#             f"📰 *{translated_title}*\n\n"
#             f"🔗 [Читать подробнее]({news_item['url']})"
#         )
#         if news_item["image"]:
#             await update.message.reply_photo(news_item["image"], caption=message_text, parse_mode="Markdown")
#         else:
#             await update.message.reply_text(message_text, parse_mode="Markdown")
