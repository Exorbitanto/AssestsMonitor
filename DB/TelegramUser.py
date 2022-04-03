from DB.database import Base, Session
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Text


class TelegramUser(Base):
    __tablename__ = 'telegram_users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    binance_key = Column(Text, nullable=False)
    debank_key = Column(Text)
    registration_date = Column(Date(), default=datetime.now)

    def __init__(self, id=None, first_name="", last_name="", binance_key="", debank_key="", session=None):
        self.session = session or Session()
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.binance_key = binance_key
        self.debank_key = debank_key
        # self.registration_date = datetime.now


    def __repr__(self):
        return f"{self.first_name}, {self.last_name}, registered on {self.registration_date}"

    def __str__(self):
        return repr(self)

    def find_or_register_new_user(self, id, first_name, last_name, binance_key):
        user = self.get_user(id)
        if user != None:
            return user
        else:
            return self.register_new_user(id, first_name, last_name, binance_key)

    def register_new_user(self, id, first_name, last_name, binance_key):
        my_user = TelegramUser(
            id=id,
            first_name=first_name,
            last_name=last_name,
            binance_key=binance_key,
        )

        self.session.add(my_user)  # Add user to the session
        self.session.commit()  # Save changes to the database
        # self.session.close()

        return my_user

    def get_user(self, id):
        return None if self.session.query(TelegramUser).count() == 0 else self.session.query(TelegramUser).filter(
            TelegramUser.id == id).one()


Base.metadata.create_all()
