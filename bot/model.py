import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib
import spacy
import numpy as np

nlp = spacy.load("ru_core_news_md")

def vectorize(text):
    doc = nlp(text)
    return doc.vector

df1 = pd.read_csv("chatbot_dataset.csv")
df2 = pd.read_csv("greeting_farewell_extended.csv")

df = pd.concat([df1, df2])

X = np.array([vectorize(text) for text in df["text"]])
y = df["intent"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression()

model.fit(X, y)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

joblib.dump(model, "intent_model.pkl")