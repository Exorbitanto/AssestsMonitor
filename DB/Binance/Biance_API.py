from binance import Client
from constants import BINANCE_SECRET_KEY, API_KEY
from datetime import datetime

# print(info["code"])  # status code
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


def try_api_key(API_KEY, SECRET_KEY):
    client = Client(API_KEY, SECRET_KEY)
    try:
        return [{"status": 200}, {"data_load": client.get_account_snapshot(type='SPOT')}]
    except Exception as ex:
        return [{"status": "error"}, {"error_text": ex}]
