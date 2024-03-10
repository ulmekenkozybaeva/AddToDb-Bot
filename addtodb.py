import telebot
import mysql.connector

bot = telebot.TeleBot('token')
channel_id = 'channel id'
fake_db = []

db = mysql.connector.connect(
    host="your host",
    user="your username",
    password="your password",
    database="database name"
)

cursor = db.cursor()


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome to the Authorization Bot\nyou should /register"
                          " if you want to freely use this bot".title())


@bot.message_handler(commands=['Register'])
def register(message):
    chat_id = message.chat.id
    q1 = bot.send_message(chat_id, "Enter Your First Name")
    bot.register_next_step_handler(q1, enter_first_name)


def enter_first_name(message):
    fake_db.append(message.text)
    q2 = bot.reply_to(message, "<b>enter</b> your last name".title(), parse_mode='HTML')
    bot.register_next_step_handler(q2, enter_last_name)


def enter_last_name(message):
    fake_db.append(message.text)
    q3 = bot.reply_to(message, "enter your phone number. should started with +998-".title())
    bot.register_next_step_handler(q3, enter_phone_number)


def enter_phone_number(message):
    fake_db.append(message.text)
    q4 = bot.reply_to(message, "enter your message".title())
    bot.register_next_step_handler(q4, enter_message)


def enter_message(message):
    fake_db.append(message.text)
    q5 = bot.reply_to(message, "Send your photo".title())
    bot.register_next_step_handler(q5, handle_photo)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    fake_db.append(message.photo[-1].file_id)

    # replace the 'database' to your database name
    sql = "INSERT INTO database (First_Name, Last_Name, Phone_Number, Message, User_Photo) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, fake_db)
    db.commit()

    combined_message = "\n".join(fake_db[:-1])
    bot.reply_to(message, f"Data successfully sent to the database")

    bot.send_photo(chat_id=channel_id, photo=downloaded_file, caption=combined_message)

    fake_db.clear()


bot.polling()
