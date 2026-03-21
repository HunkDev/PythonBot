from datetime import datetime
import db
import func
import re

if __name__ == "__main__":
    db.init_db()
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_input = input("Вы: ")

        response = func.process_message(user_input)

        db.log_message(now, user_input, response)
        print(f"{now} Бот: {response}")

        text = (user_input + " " + response).lower()

        if re.search(r"\b(пока|до свидания|увидимся|бай|bye)\b", text):
            break