from datetime import datetime
import requests
import db
import spacy
import key
import states

nlp = spacy.load("ru_core_news_md")
WEATHER_INTENT_WORDS = {"погода", "погоду", "температура", "градус", "градусов", "прогноз", "холодно", "жарко", "дождь", "снег", "солнце"}

global current_user
current_user = None

def handle_user(user):
    id = hash(user) % 10000
    result = db.get_user(id)
    if result:
        return result
    else:
        return None

def handle_greeting(match=None):
    global current_user
    user = handle_user(current_user)
    if user:
        return f"С возвращением, {user}! Чем могу помочь?"
    else:
        return "Здравствуйте! Чем могу помочь?"

def handle_farewell(match=None):
    global current_user
    user = handle_user(current_user)
    if user:
        return f"До встречи, {user}! хорошего дня!"
    else:
        return "До свидания! Хорошего дня!"

def handle_name(match):
    global current_user
    name = match.group(1)
    user_id = hash(name) % 10000
    db.save_user(user_id, name)
    current_user = name
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

def extract_city(doc):
    for ent in doc.ents:
        if ent.label_ == "LOC":
            lemma = ent[0].lemma_
            if " " in lemma or "-" in lemma:
                parts = [p.title() for p in lemma.split()]
                return " ".join(parts)
            return lemma.title()

    for token in doc:
        if token.pos_ == "PROPN" and token.ent_type_ == "":
            lemma = token.lemma_.title()
            if len(lemma) > 3:
                return lemma
    
    return None

def has_weather_intent(text: str) -> bool:
    text_lower = text.lower()
    return any(word in text_lower for word in WEATHER_INTENT_WORDS)

def get_weather(location):
    url = "http://api.weatherstack.com/current"
    querystring = {"access_key": key.KEY, "query": location, "units": "m"}

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

def process_message(text: str):
    text = text.strip()
    if not text:
        return "Напиши что-нибудь"

    message = states.manage_state(text)
    if(message):
        return message
    else:
        return "Что-то пошло не так"