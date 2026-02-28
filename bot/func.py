import patterns
from datetime import datetime
import requests
import db


def handle_greeting(match=None):
    return "Здравствуйте! Чем могу помочь?"

def handle_farewell(match=None):
    return "До свидания! Хорошего дня!"

def handle_name(match):
    name = match.group(1)
    user_id = hash(name) % 10000
    db.save_user(user_id, name)
    return f"Приятно познакомиться, {name}!"

def get_current_time(match=None):
    now = datetime.now()
    return f"Текущее время: {now.strftime('%H:%M:%S')}"

def get_current_date(param=None):
    now = datetime.now()
    if param and param.lower() == "день":
        return f"Сегодня {now.day} число."
    elif param and param.lower() == "месяц":
        return f"Сейчас {now.strftime('%B')}."
    elif param and param.lower() == "год":
        return f"Сейчас {now.year} год."
    else:
        return f"Сегодня {now.strftime('%d %B %Y')}."
    
def handle_math(a, b, operation):
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        return "Пожалуйста, введите числовые значения для a и b."
    
    if operation == "+":
        return f"Результат: {a + b}"
    elif operation == "-":
        return f"Результат: {a - b}"
    elif operation == "*":
        return f"Результат: {a * b}"
    elif operation == "/":
        if b == 0:
            return "Ошибка: деление на ноль невозможно."
        return f"Результат: {a / b}"
    else:
        return "Неизвестная операция. Пожалуйста, используйте '+', '-', '*' или '/'."
  
def get_weather(location):
    url = "http://api.weatherstack.com/current"
    querystring = {"access_key": "d0eba72320d48e0dcb44f69a8dd98526", "query": location, "units": "m"}

    try:
        response = requests.get(url, params=querystring)
        response.raise_for_status()
    except requests.RequestException:
        print(f"Ошибка при запросе к API: {response.status_code}")
        return "Ошибка получения данных о погоде."

    data = response.json()

    temp = data["current"]["temperature"]
    description = data["current"]["weather_descriptions"][0]
    wind = data["current"]["wind_speed"]

    return f"Погода в {location}: {temp}°C, {description}, скорость ветра: {wind} км/ч."

def process_message(message: str):
    message = message.strip()
    for pattern, handler in patterns.patterns:
        match = pattern.match(message)
        if match:
            return handler(match)
    return "Извините, я не понимаю. Пожалуйста, попробуйте другое сообщение."