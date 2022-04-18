from binance import Client
from DB.TelegramUserService import TelegramUserService


def try_api_key(API_KEY, SECRET_KEY):
    client = Client(API_KEY, SECRET_KEY)
    try:
        return [{"status": 200}, {"data_load": client.get_account_snapshot(type='SPOT')}]
    except Exception as ex:
        return [{"status": "error"}, {"error_text": ex}]

def request_spot_data_for_range(telegram_id, start_date:int, end_date:int):
    user = TelegramUserService().get_user(telegram_id)
    client = Client(user.binance_key, user.binance_secret_key)
    return client.get_account_snapshot(type='SPOT', start_date=start_date, end_date=end_date)