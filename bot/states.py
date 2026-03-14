import patterns
import func
import spacy

nlp = spacy.load("ru_core_news_md")
current_state = "START"

def manage_state(text):
    global current_state
    doc = nlp(text)

    for pattern, handler in patterns.patterns:
        match = pattern.match(text)
        if match:
            result = handler(match)
            current_state = "START"
            return result

    if current_state == "START":

        if func.has_weather_intent(text) and not func.extract_city(doc):
            current_state = "WAIT_CITY"
            return "В каком городе хочешь узнать погоду?"

        city = func.extract_city(doc)
        if func.has_weather_intent(text) and city:
            current_state = "START"
            return func.get_weather(city)

        return "Я не понимаю"

    elif current_state == "WAIT_CITY":
        
        city = func.extract_city(doc)
        
        if city:
            current_state = "START"
            return func.get_weather(city)
        else:
            return "Не смог определить город\nНапиши название города, пожалуйста (например: Москва, Питер, Новосибирск)"