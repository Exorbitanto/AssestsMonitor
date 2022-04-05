from binance import Client
from constants import BINANCE_SECRET_KEY, API_KEY
from datetime import datetime




def try_api_key(API_KEY, SECRET_KEY):
    client = Client(API_KEY, SECRET_KEY)
    try:
        return [{"status": 200}, {"data_load": client.get_account_snapshot(type='SPOT')}]
    except Exception as ex:
        return [{"status": "error"}, {"error_text": ex}]
