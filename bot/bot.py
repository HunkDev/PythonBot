from datetime import datetime
import db
import func
import re
from silero import silero_tts
from playsound3 import playsound

if __name__ == "__main__":
    db.init_db()
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_input = input("Вы: ")

        response = func.process_message(user_input)

        model, text = silero_tts(language='ru',
                                 speaker='v5_ru')
        audio = model.save_wav(text=response,
                             speaker="eugene",
                             sample_rate=48000)

        playsound("test.wav")
        db.log_message(now, user_input, response)
        print(f"{now} Бот: {response}")

        text = (user_input + " " + response).lower()

        if re.search(r"\b(пока|до свидания|увидимся|бай|bye)\b", text):
            break