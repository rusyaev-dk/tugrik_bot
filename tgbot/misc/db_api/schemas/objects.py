from sqlalchemy import Column, BigInteger, sql, Integer, String, ARRAY

from tgbot.misc.db_api.db_gino import TimeBaseModel


class User(TimeBaseModel):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100))
    balance = Column(Integer)
    referral = Column(BigInteger)
    identificator = Column(String(100))
    friends = Column(ARRAY(Integer), default=[])

    query: sql.Select


class UserProperty(TimeBaseModel):
    __tablename__ = "users_property"

    owner_id = Column(BigInteger, primary_key=True)
    owner_name = Column(String(100))
    owner_balance = Column(Integer)
    horses = Column(ARRAY(String(100)), default=[])

    query: sql.Select


class Administrator(TimeBaseModel):
    __tablename__ = "admins"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100))
    feedback_user_id = Column(BigInteger)

    query: sql.Select
