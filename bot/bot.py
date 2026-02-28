from datetime import datetime
import func

if __name__ == "__main__":
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_input = input("Вы: ")
        if user_input.lower() in ["пока", "до свидания", "увидимся"]:
            response = func.process_message(user_input)
            func.log_message(now, user_input, response)
            print(f"{now} Бот: {response}")
            break
        response = func.process_message(user_input)
        print(f"{now} Бот: {response}")
        func.log_message(now, user_input, response)