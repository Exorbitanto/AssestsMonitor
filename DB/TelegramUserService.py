from DB.database import Session
from DB.TelegramUser import TelegramUser
from DB.Binance.Biance_API import try_api_key

class TelegramUserService:

    def __init__(self, session=None):
        self.session = session or Session()

    def find_or_register_new_user(self, telegram_id, first_name, last_name, binance_key, binance_secret_key):
        user = self.get_user(telegram_id)
        if user != None:
            return "already_exists"
        else:
            try_keys = try_api_key(binance_key, binance_secret_key)
            if try_keys[0]["status"] == 200:
                try:
                    self.register_new_user(telegram_id, first_name, last_name, binance_key, binance_secret_key)
                    return "user_registered_successfully"
                except Exception as ex:
                    return f"error {ex}"
            else:
                return try_keys[1]["error_text"]

    def register_new_user(self, telegram_id, first_name, last_name, binance_key="", binance_secret_key = "", debank_wallet=""):
        my_user = TelegramUser(
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            binance_key=binance_key,
            binance_secret_key = binance_secret_key,
            debank_wallet=debank_wallet
        )

        self.session.add(my_user)  # Add user to the session
        self.session.commit()  # Save changes to the database

        return my_user

    def get_user(self, telegram_id):
        return None if self.session.query(TelegramUser).count() == 0 else self.session.query(TelegramUser).filter(
            TelegramUser.telegram_id == telegram_id).one()

    def add_debank_wallet(self, telegram_id, first_name, last_name, debank_wallet):
        user = self.get_user(telegram_id)

        if user != None:
            user.debank_wallet = debank_wallet
            self.session.commit()  # Save changes to the database
            return "debank_wallet_registered_successfully"
        else:
            self.register_new_user(telegram_id, first_name, last_name, debank_wallet = debank_wallet)
            return "user_registered_successfully"



