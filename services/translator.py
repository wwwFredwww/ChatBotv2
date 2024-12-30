from deep_translator import GoogleTranslator

def translate_text(text, dest_language="ru"):
    try:
        return GoogleTranslator(source='auto', target=dest_language).translate(text)
    except Exception as e:
        print(f"Ошибка перевода: {e}")
        return "❌ Перевод временно недоступен."
