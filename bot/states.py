import patterns
import func
import spacy
import joblib

model = joblib.load("intent_model.pkl")

nlp = spacy.load("ru_core_news_md")
current_state = "START"

def predict_intent(text):
    doc = nlp(text)
    vector = doc.vector
    intent = model.predict([vector])[0]

    if hasattr(model, "predict_proba"):
        proba = model.predict_proba([vector]).max()
    else:
        proba = 1.0
    
    return intent, proba

def handle_ml_intent(intent, text):
    if intent == "greeting":
        return func.handle_greeting()

    elif intent == "farewell":
        return func.handle_farewell()

    elif intent == "time":
        return func.get_current_time()

    elif intent == "date":
        return func.get_current_date()

    elif intent == "day":
        return func.get_current_date("день")

    elif intent == "month":
        return func.get_current_date("месяц")

    elif intent == "year":
        return func.get_current_date("год")
    elif intent == "name":
        return func.handle_name(text)

    return "Я не уверен, что понял тебя"

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

        intent, confidence = predict_intent(text)

        print(confidence)
        if confidence > 0.6:
            return handle_ml_intent(intent, text)

        return "Я не понимаю"

    elif current_state == "WAIT_CITY":
        
        city = func.extract_city(doc)
        
        if city:
            current_state = "START"
            return func.get_weather(city)
        else:
            return "Не смог определить город\nНапиши название города, пожалуйста (например: Москва, Питер, Новосибирск)"