import telebot

from DB.database import Session
from constants import TEl_BOT_KEY
from DB.TelegramUser import TelegramUser


bot = telebot.TeleBot(TEl_BOT_KEY)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am Crypto Assets Monitor.
To register, please use the /register command
""")


# Handle '/register'
@bot.message_handler(commands=['register'])
def register_new_user(message):
    session = Session()
    user = TelegramUser(session = session).find_or_register_new_user(id=message.from_user.id,
                                                  first_name=message.from_user.first_name,
                                                  last_name=message.from_user.last_name,
                                                  binance_key=message.text.replace("/register", "").strip()
                                                  )
    print(user.first_name)
    session.close()


# print(message.text)
# print(message.from_user.id)
# print(message.from_user.first_name)
# print(message.from_user.last_name)


bot.polling()
