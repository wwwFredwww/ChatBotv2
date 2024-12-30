import requests

def get_latest_news(category="technology"):
    try:
        api_key = "5c576dc45ba04d9d9667093c7329705b"
        url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "ok":
            return None

        return [
            {
                "title": article.get("title"),
                "image": article.get("urlToImage"),
                "url": article.get("url")
            }
            for article in data.get("articles", [])[:5]
        ]
    except Exception as e:
        print(f"Ошибка получения новостей: {e}")
        return None
