import telebot

from DB.database import Session
from constants import TEl_BOT_KEY
from DB.TelegramUserService import TelegramUserService

bot = telebot.TeleBot(TEl_BOT_KEY)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am Crypto Assets Monitor.\
To register, please use the /register command
""")


# Handle '/register'
@bot.message_handler(commands=['register'])
def register_new_user(message):
    binance_keys = message.text.replace("/register", "").strip().split(" ")
    if len(binance_keys) !=2:
        bot.reply_to(message,
                     """Hi there, I am Crypto Assets Monitor.To register, please use the /register
                     command followed by your Binance API key, a space and your Secret Binance Key""")

    session = Session()
    register_binance_key_result = TelegramUserService(session).find_or_register_new_user(
        telegram_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        binance_key=binance_keys[0],
        binance_secret_key=binance_keys[1]
        )
    session.close()
    bot.reply_to(message, register_binance_key_result)


# Handle '/add_debank_wallet'
@bot.message_handler(commands=['add_debank_wallet'])
def add_debank_wallet(message):
    debank_wallet = message.text.replace("/add_debank_wallet", "").strip()
    if debank_wallet == "":
        bot.reply_to(message,
                     "Hi there, I am Crypto Assets Monitor.To register, please use the /add_debank_wallet command followed by your debank wallet ID")

    session = Session()
    register_debank_wallet_result = TelegramUserService(session).add_debank_wallet(
        telegram_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        debank_wallet=debank_wallet
        )
    session.close()
    bot.reply_to(message, register_debank_wallet_result)


bot.polling()
