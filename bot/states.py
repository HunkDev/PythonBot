import patterns
import func
import spacy
import torch
import pandas as pd
import random
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_PATH = r"c:\Users\serge\source\repos\Python\AI\bot\intent_model"

df = pd.read_csv(r"c:\Users\serge\source\repos\Python\AI\bot\extended_intent_dataset.csv")

labels = df["intent"].unique()

label_map = {i: label for i, label in enumerate(labels)}
reverse_label_map = {label: i for i, label in label_map.items()}
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

nlp = spacy.load("ru_core_news_md")

current_state = "START"


def predict_intent(text: str):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=1)
        
        predicted_class = torch.argmax(logits, dim=1).item()
        confidence = probs.max().item()
        top3_probs, top3_indices = torch.topk(probs, 3)
    
    intent = label_map.get(predicted_class, "unknown")
    
    print(f"Intent: {intent} | Confidence: {confidence:.4f} | Top3: "
          f"{[(label_map.get(i.item(), 'unknown'), p.item()) for i, p in zip(top3_indices[0], top3_probs[0])]}")
    
    return intent, confidence


def handle_ml_intent(intent: str, text: str):
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

    elif intent == "help":
        features = [
        "Приветствия и прощания",
        "Текущее время",
        "Дата, день, месяц, год",
        "Простые вычисления",
        "Погода по городу",
        "Небольшой разговор"
        ]

        return "Я умею:\n" + "\n".join(f"• {f}" for f in features)
    
    elif intent == "smalltalk":
        responses = [
        "Всё хорошо 🙂",
        "Отлично, спасибо!",
        "Работаю без перерыва 😄"
        ]
        return random.choice(responses)

    return "Я не уверен, что понял тебя"


def manage_state(text: str):
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

        with torch.no_grad():
            outputs = model(**tokenizer(text, return_tensors="pt", truncation=True))
            probs = torch.softmax(outputs.logits, dim=1)
            confidence = probs.max().item()

        print(f"Intent: {intent} | Confidence: {confidence:.4f}")

        if confidence > 0.75:
            return handle_ml_intent(intent, text)
        else:
            return "Извини, я не совсем понял. Можешь перефразировать? Например: 'Какая погода в Москве?' или 'Привет'."

    elif current_state == "WAIT_CITY":
        city = func.extract_city(doc)
        
        if city:
            current_state = "START"
            return func.get_weather(city)
        else:
            return "Не смог определить город.\nНапиши название города, пожалуйста (например: Москва, Питер, Новосибирск)"