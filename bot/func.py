import patterns
from datetime import datetime


def handle_greeting(match=None):
    return "Здравствуйте! Чем могу помочь?"

def handle_farewell(match=None):
    return "До свидания! Хорошего дня!"

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

def process_message(message: str):
    message = message.strip()
    for pattern, handler in patterns.patterns:
        match = pattern.match(message)
        if match:
            return handler(match)
    return "Извините, я не понимаю. Пожалуйста, попробуйте другое сообщение."

def log_message(time, user, bot):
    with open("chat_log.txt", "a", encoding = "utf-8") as log_file:
        log_file.write(f"User: {time} {user}\n")
        log_file.write(f"Bot: {time} {bot}\n")
        log_file.write("-" * 40 + "\n")