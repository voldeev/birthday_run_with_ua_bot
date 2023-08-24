#6543209608:AAG5TWwy8q9Rkc93qyyRIzdnDiBUBjy9qrM

from telegram.ext import Updater, MessageHandler, CallbackContext, Filters
import sqlite3
import datetime

def save_user_data(update, context):
    user = update.message.from_user
    user_id = user.id
    username = user.username
    phone_number = update.message.text
    context.user_data[user_id] = phone_number

    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO users (user_id, username, phone_number) VALUES (?, ?, ?)',
                   (user_id, username, phone_number))

    conn.commit()
    conn.close()

    update.message.reply_text("Введіть дату народження у форматі ДД.ММ (наприклад, 24.08).")

def set_birthday(update, context):
    user = update.message.from_user
    user_id = user.id
    user_text = update.message.text

    try:
        birthday = datetime.datetime.strptime(user_text, '%d.%m').date()
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()

        cursor.execute('UPDATE users SET birthday = ? WHERE user_id = ?', (birthday, user_id))

        conn.commit()
        conn.close()

        update.message.reply_text("Дата народження збережена. Очікуйте на привітання!")
    except ValueError:
        update.message.reply_text("Невірний формат дати. Введіть дату у форматі ДД.ММ (наприклад, 24.08).")

def check_birthday(context):
    today = datetime.date.today()
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT user_id FROM users WHERE strftime("%d-%m", birthday) = ?', (today.strftime("%d-%m"),))
    users_today = cursor.fetchall()

    for user_id in users_today:
        context.bot.send_message(user_id[0], f"З Днем народження! 🎉🎂")

    conn.close()

def main():
    api_key = "6543209608:AAG5TWwy8q9Rkc93qyyRIzdnDiBUBjy9qrM"  # Підставте сюди ваш API-ключ
    updater = Updater(token=api_key, use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, save_user_data))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'^\d{2}\.\d{2}$'), set_birthday))

    job_queue = updater.job_queue
    job_queue.run_daily(check_birthday, time=datetime.time(hour=9, minute=0, second=0))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
