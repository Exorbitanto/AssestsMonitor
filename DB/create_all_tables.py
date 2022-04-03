from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer

engine = create_engine(r'sqlite:///C:\Users\Eugen\PycharmProjects\AssestsMonitor\AssestsMonitor.db')

# MetaData object will hold database related information
meta = MetaData(engine)

users = Table(
    'telegram_users', meta,  # Meta passed as argument here
    Column('telegram_id', Integer, primary_key=True),
    Column('first_name', String),
    Column('last_name', String),
    Column('binance_key', String),
    Column('debank_key', String),

)

meta.create_all()