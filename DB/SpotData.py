from DB.database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Float


class SpotData(Base):
    __tablename__ = 'assets_in_time'

    date = Column(Date(), primary_key=True)
    currency_symbol = Column(String(10), primary_key=True)
    available_amount = Column(Float, default=0)
    locked_amount = Column(Float, default=0)

    def __init__(self, date=datetime.now(), currency_symbol="", available_amount=0, locked_amount=0):
        self.date = date
        self.currency_symbol = currency_symbol
        self.available_amount = available_amount
        self.locked_amount = locked_amount

    def __repr__(self):
        return f"On {self.date}, {self.available_amount} {self.currency_symbol} were available and {self.locked_amount} were locked"

    def __str__(self):
        return repr(self)


Base.metadata.create_all()
