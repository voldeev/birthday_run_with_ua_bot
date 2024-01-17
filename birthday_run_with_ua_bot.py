import json
from datetime import datetime
import random
import time
from telegram.ext import Updater, CallbackContext

# Зчитування даних з JSON-файлу
def load_user_data():
    try:
        with open('user_data.json', 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return []

def send_birthday_greetings_to_chat(users: list, context: CallbackContext):
    today_day, today_month = datetime.now().strftime('%d/%m').split('/')

    for user in users:
        user_birthday = user['birthday']
        user_nickname = user['telegram_nickname']
        user_insta_profile = user['instagram_link']
        user_gender = user.get('gender', 'unknown')

        user_day, user_month, _ = user_birthday.split('/')

        if user_day == today_day and user_month == today_month:
            chat_id = user['user_id']

            non_birthday_greetings = [
                "🏃‍♂️ Нехай кожен день буде для тебе новим забігом до перемог!\n",
                "🌟 Зичимо яскравих тренувань та багато неймовірних досягнень!\n",
                "👣 Нехай кожен крок приносить тобі радість та задоволення!\n",
                "🏆 Бажаємо впевненості на трасі та сил для подолання будь-яких викликів!\n",
                "🌞 Нехай сонце завжди світить на твоєму біговому шляху!\n",
                "🌿 Зичимо бігової гармонії та здоров'я на кожному кроці!\n",
                "👟 Будь завжди швидким, як вітер, та стійким, як гори!\n",
                "🌺 Нехай кожен метр твого бігу буде наповнений позитивом та вдячністю!\n",
                "🚀 Бажаємо надзвичайних здібностей та вражаючих рекордів!\n",
                "🌄 Нехай твій біг прокладає шлях до нових горизонтів!\n",
                "💪 Здоров'я, сили та нескінченної енергії на трасі життя!\n",
                "🌈 Нехай кожен біговий день буде для тебе святом радості!\n",
                "🌳 Завжди знаходь підтримку у природі та своїх власних можливостях!\n",
                "🌟 Біжи так, наче кожен день - це новий старт до перемог!\n",
                "🎊 Зичимо бігового екстазу та відчуття свободи на кожному кілометрі!\n"
            ]  # Додайте кому після останнього елемента, якщо додаєте нові рядки

            birthday_greetings_for_men = [
                "🏃‍♂️ Вітаємо тебе, бігуне, з чудовим Днем народження!\n",
                "🎈 Нехай твої ноги завжди будуть швидкими, а серце - міцним!\n",
                "🎂 З Днем народження, майбутній чемпіоне!\n",
                "🏆 Вітаємо з Днем народження, майстерність та витривалість бігуна!\n",
                # Додавайте інші рядки з "з Днем народження"
            ]

            birthday_greetings_for_women = [
                "🏃‍♀️ Вітаємо тебе, ранерко, з чудовим Днем народження!\n",
                "🎈 Нехай твої ноги завжди будуть швидкими, а серце - міцним!\n",
                "🎂 З Днем народження, майбутня чемпіонко!\n",
                "🏆 Вітаємо з Днем народження, майстерність та витривалість ранерко!\n",
                # Додавайте інші рядки з "з Днем народження" для жінок
            ]

            # Вибираємо 4 рандомні рядки без "з Днем народження"
            selected_non_birthday_greetings = random.sample(non_birthday_greetings, 4)

            # Початок привітання з інформацією про користувача
            greeting_prefix = f"Привіт, {user_nickname} ({user['first_name']} {user['last_name']})!\n "

            # Розділ привітань
            first_part_of_greeting = greeting_prefix + " ".join(selected_non_birthday_greetings)

            # Ініціалізація selected_birthday_greeting пустим рядком
            selected_birthday_greeting = ""

            # Вибір рандомного привітання з Днем народження
            if user_gender.lower() == 'male':
                selected_birthday_greeting = random.choice(birthday_greetings_for_men)
            elif user_gender.lower() == 'female':
                selected_birthday_greeting = random.choice(birthday_greetings_for_women)
            else:
                selected_birthday_greeting = random.choice(birthday_greetings_for_men + birthday_greetings_for_women)

            # Додаємо вибрані привітання в повідомлення
            message = first_part_of_greeting
            if selected_birthday_greeting:
                message += " " + selected_birthday_greeting

            # Додаємо закінчення повідомлення
            message += "Завжди з тобою RUN WITH UKRAINE🥳🎂\n"
            message += f"Можете привітати в Інстаграм: {user_insta_profile} 📸🔥"

            context.bot.send_message(chat_id="-1001267994264", text=message)
            print(f"Sending birthday greetings to {user['first_name']} {user['last_name']}")
            print("Birthday greetings sent successfully!")



def main():
    user_data = load_user_data()
    updater = Updater("ваш_токен", use_context=True)  # Замініть на ваш токен

    # Отримуємо поточний час
    current_time = datetime.now().strftime("%H:%M:%S")

    # Задаємо час, коли має відправитися повідомлення
    scheduled_time = "10:00:00"

    # Очікуємо на настання запланованого часу
    while current_time < scheduled_time:
        current_time = datetime.now().strftime("%H:%M:%S")
        time.sleep(1)

    send_birthday_greetings_to_chat(user_data, updater)
    updater.start_polling()

if __name__ == '__main__':
    main()
