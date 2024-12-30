from flask import Flask, request
from threading import Thread

# Инициализация Flask-приложения
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"  # Текст, который будет виден при доступе к серверу

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     # Получаем обновление Telegram
#     json_data = request.get_json(force=True)
#     app.bot.process_update(json_data)
#     return 'OK', 200

# Функция для запуска Flask-сервера
def run():
    app.run(host='0.0.0.0', port=8080)

# Функция для запуска Flask-сервера в отдельном потоке
def keep_alive():
    t = Thread(target=run)
    t.start()

# # Функция для регистрации вебхука
# def register_webhook(app):
#     # Передаем бота в Flask-приложение
#     app.bot = app
#
#     # Настраиваем вебхук
#     WEBHOOK_URL = "https://your-app-name.onrender.com/webhook"  # Замените на ваш URL
#     app.bot.bot.set_webhook(url=WEBHOOK_URL)
#     print(f"Webhook зарегистрирован: {WEBHOOK_URL}")
