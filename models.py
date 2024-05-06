from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text, DECIMAL, BLOB
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'User'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(255))
    user_last_name = Column(String(255))
    user_mail = Column(String(255))
    user_date = Column(Date)
    user_password = Column(String(45))
    user_stars = Column(Integer)
    uid_firebase = Column(String(255))
    products = relationship("Product")

# class Message(Base):
#     __tablename__ = 'message'

#     sms_id = Column(Integer, primary_key=True, autoincrement=True)
#     sms_content = Column(String(255))
#     sms_date = Column(Date)
#     sms_sender = Column(Integer, ForeignKey('User.user_id'))
#     sms_recipient = Column(Integer, ForeignKey('User.user_id'))

class Categorie(Base):
    __tablename__ = 'categorie'

    cate_id = Column(Integer, primary_key=True)
    cate_name = Column(String(45))

    products = relationship("Product")

class Product(Base):
    __tablename__ = 'product'

    prod_id = Column(Integer, primary_key=True)
    prod_name = Column(String(255))
    prod_price = Column(DECIMAL(10, 2))
    prod_desc = Column(String(255))
    prod_img = Column(Text)
    prod_cate_id = Column(Integer, ForeignKey('categorie.cate_id'))
    prod_user_id = Column(Integer, ForeignKey('User.user_id'))

    category = relationship("Categorie")
    user = relationship("User")

class Terms(Base):
    __tablename__ = 'terms'

    term_date = Column(Date, primary_key=True)
    term_content = Column(String(1000))
