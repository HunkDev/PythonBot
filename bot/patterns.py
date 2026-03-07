import re
import func

patterns = [
    (re.compile(r"^(привет|здравствуйте|добрый день)$", re.IGNORECASE), lambda m: func.handle_greeting()),
    (re.compile(r"^(пока|до свидания|увидимся)$", re.IGNORECASE), lambda m: func.handle_farewell()),
    (re.compile(r"^который час\??$", re.IGNORECASE), lambda m: func.get_current_time()),
    (re.compile(r"^какая (сегодня|сейчас) дата\??$", re.IGNORECASE), lambda m: func.get_current_date()),
    (re.compile(r"^какой (сегодня|сейчас) день\??$", re.IGNORECASE), lambda m: func.get_current_date("день")),
    (re.compile(r"^какой (сегодня|сейчас) месяц\??$", re.IGNORECASE), lambda m: func.get_current_date("месяц")),
    (re.compile(r"^какой (сегодня|сейчас) год\??$", re.IGNORECASE), lambda m: func.get_current_date("год")),
    (re.compile(r"^([0-9]+(?:\.[0-9]+)?)\s*([+\-*/])\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE), lambda m: func.handle_math(m.group(1), m.group(3), m.group(2))),
    #(re.compile(r"^Погода в (.+)$", re.IGNORECASE), lambda m: func.get_weather(m.group(1))),
    (re.compile(r"^Меня зовут (.+)$", re.IGNORECASE), lambda m: func.handle_name(m)),
]