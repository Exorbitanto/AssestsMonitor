from datetime import datetime, date, timedelta

from DB.TelegramUserService import TelegramUserService
from DB.database import Session
from DB.SpotData import SpotData
from binance import Client


class SpotDataService:
    def __init__(self, session=None):
        self.session = session or Session()

    def process_and_register_spot_data(self, telegram_id, binance_spot_data):
        if binance_spot_data["code"] == 200:
            # data_load = binance_spot_data[1]["data_load"]
            for element in binance_spot_data["snapshotVos"]:
                date = (datetime.utcfromtimestamp(element["updateTime"] / 1000)).date()
                for currency in element["data"]["balances"]:
                    currency_symbol = currency["asset"]  # currency name
                    available_amount = currency["free"]  # avaialble amount
                    locked_amount = currency["locked"]  # locked amount
                    self.register_new_data(telegram_id, date, currency_symbol, available_amount,
                                           locked_amount)
                self.session.commit()  # Save changes to the database

    def register_new_data(self, telegram_id, date, currency_symbol, available_amount, locked_amount):

        if not self.session.query(SpotData).filter(SpotData.telegram_id == telegram_id, SpotData.date == date,
                                                     SpotData.currency_symbol == currency_symbol).all():

            my_data = SpotData(
                telegram_id=telegram_id,
                date=date,
                currency_symbol=currency_symbol,
                available_amount=available_amount,
                locked_amount=locked_amount
            )

            self.session.add(my_data)  # Add data to the session

    def get_all_assets_for_date(self, telegram_id, date):
        result = self.session.query(SpotData).filter(SpotData.telegram_id == telegram_id, SpotData.date == date,
                                                     SpotData.available_amount != 0).all()
        if not result:
            data_to_write = SpotDataService.request_spot_data_for_range(telegram_id, date, date)
            self.process_and_register_spot_data(telegram_id, data_to_write)
            result = self.session.query(SpotData).filter(SpotData.telegram_id == telegram_id, SpotData.date == date,
                                                         SpotData.available_amount != 0).all()
        return result


    def get_and_compare_assets_for_last_2_days(self, telegram_id):

        yesterday_date = date.today() - timedelta(days=1)
        two_days_ago_date = date.today() - timedelta(days=2)
        yesterday = self.get_all_assets_for_date(telegram_id, yesterday_date)
        two_days_ago = self.get_all_assets_for_date(telegram_id, two_days_ago_date)
        list_of_dicts = list()
        for yesterday_element in yesterday:
            for two_days_ago_element in two_days_ago:
                if yesterday_element.date == two_days_ago_element.date and yesterday_element.currency_symbol == two_days_ago_element.currency_symbol:
                    dict_element = {"date": yesterday_element.date, "available_yesterday": yesterday_element.available_amount, "available_2_days_ago": two_days_ago_element.available_amount}
                    list_of_dicts.append(dict_element)
        return list_of_dicts

    @staticmethod
    def try_api_key(API_KEY, SECRET_KEY):
        client = Client(API_KEY, SECRET_KEY)
        try:
            return [{"status": 200}, {"data_load": client.get_account_snapshot(type='SPOT')}]
        except Exception as ex:
            return [{"status": "error"}, {"error_text": ex}]

    @staticmethod
    def request_spot_data_for_range(telegram_id, start_date: int, end_date: int):
        user = TelegramUserService().get_user(telegram_id)
        client = Client(user.binance_key, user.binance_secret_key)
        return client.get_account_snapshot(type='SPOT', start_date=start_date, end_date=end_date)
