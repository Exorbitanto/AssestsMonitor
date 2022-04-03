from DB.database import Session
from DB.TelegramUser import TelegramUser


class TelegramUserService:

    def __init__(self, session=None):
        self.session = session or Session()

    def find_or_register_new_user(self, telegram_id, first_name, last_name, binance_key):
        user = self.get_user(telegram_id)
        if user != None:
            return user
        else:
            return self.register_new_user(telegram_id, first_name, last_name, binance_key)

    def register_new_user(self, telegram_id, first_name, last_name, binance_key):
        my_user = TelegramUser(
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            binance_key=binance_key,
        )

        self.session.add(my_user)  # Add user to the session
        self.session.commit()  # Save changes to the database
        self.session.close()

        return my_user

    def get_user(self, telegram_id):
        return None if self.session.query(TelegramUser).count() == 0 else self.session.query(TelegramUser).filter(
            TelegramUser.telegram_id == telegram_id).one()
