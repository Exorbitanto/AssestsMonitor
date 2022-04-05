from datetime import datetime

from DB.database import Session
from DB.SpotData import SpotData


class SpotDataService:

    @staticmethod
    def process_and_register_spot_data(binance_spot_data):
        if binance_spot_data[0]["status"] == 200:
            data_load =  binance_spot_data[1]["data_load"]
            for element in data_load["snapshotVos"]:
                date = datetime.utcfromtimestamp(element["updateTime"] / 1000)
                session = Session()
                for currency in element["data"]["balances"]:
                    currency_symbol = currency["asset"]  # currency name
                    available_amount = currency["free"]  # avaialble amount
                    locked_amount = currency["locked"] #locked amount
                    SpotDataService.register_new_data(session, date, currency_symbol, available_amount, locked_amount)
                session.commit()  # Save changes to the database
                session.close()


    @staticmethod
    def register_new_data(session, date, currency_symbol, available_amount, locked_amount):

        my_data = SpotData(
            date=date,
            currency_symbol=currency_symbol,
            available_amount=available_amount,
            locked_amount=locked_amount
        )

        session.add(my_data)  # Add data to the session



# info["snapshotVos"]  # list of dicts
# for element in info["snapshotVos"]:
#     ts = element["updateTime"] / 1000
#     print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))  # timestamp
#     element["data"]  # dict
#     print(element["data"]["totalAssetOfBtc"])  # totla in BTC
#     element["data"]["balances"]  # list of dicts with assests
#     for currency in element["data"]["balances"]:
#         print(currency["asset"])  # currency name
#         print(currency["free"])  # avaialble amount
#         print(currency["locked"])  # locked amount
#
# print(info)


