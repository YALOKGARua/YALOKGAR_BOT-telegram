import requests

WEATHER_API_KEY = '28a12b618eac488888f194053242608'
WEATHER_API_URL = 'http://api.weatherapi.com/v1/current.json'

NEWS_API_KEY = '75fd9512d3f346498df27a0e66b340a3'
NEWS_API_URL = 'https://newsapi.org/v2/top-headlines'

def get_weather(city: str) -> str:
    response = requests.get(f"{WEATHER_API_URL}?key={WEATHER_API_KEY}&q={city}")
    data = response.json()
    
    if 'current' in data:
        return (
            f"Погода в місті {city}:\n"
            f"Температура: {data['current']['temp_c']}°C\n"
            f"Стан: {data['current']['condition']['text']}\n"
            f"Вологість: {data['current']['humidity']}%\n"
        )
    else:
        return "Не вдалося отримати дані про погоду."

def get_news() -> str:
    response = requests.get(f"{NEWS_API_URL}?apiKey={NEWS_API_KEY}&country=us")
    data = response.json()
    
    if 'articles' in data and data['articles']:
        latest_news = data['articles'][0]
        return (
            f"Останні новини:\n"
            f"Заголовок: {latest_news['title']}\n"
            f"Опис: {latest_news['description']}\n"
            f"Посилання: {latest_news['url']}\n"
        )
    else:
        return "Не вдалося отримати новини."
