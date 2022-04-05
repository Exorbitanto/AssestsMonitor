from DB.database import Session
from DB.SpotData import SpotData


class SpotDataService:

    def __init__(self, session=None):
        self.session = session or Session()

    def register_new_data(self, date, currency_symbol, available_amount, locked_amount):
        my_data = SpotData(
            date=date,
            currency_symbol=currency_symbol,
            available_amount=available_amount,
            locked_amount=locked_amount
        )

        self.session.add(my_data)  # Add data to the session
        self.session.commit()  # Save changes to the database

        return my_data

    def get_data(self, telegram_id):
        pass
        # return None if self.session.query(TelegramUser).count() == 0 else self.session.query(TelegramUser).filter(
        #     TelegramUser.telegram_id == telegram_id).one()



