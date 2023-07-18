from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(UserMixin, db.Model):

    __tablename__ = 'dataUser'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(15))
    confirm_password = db.Column(db.String(15))


class Price_History(db.Model):
    #Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
    __tablename__ = 'dataETL'
    __table_args__ = {'sqlite_autoincrement': True}
    #tell SQLAlchemy the name of column and its attributes:
    id = db.Column(db.Integer, primary_key=True)
    Order_ID = db.Column(db.float)
    Product = db.Column(db.String(15), unique=True)
    Quantity_Ordered = db.Column(db.float)
    Price_Each = db.Column(db.float)
    Order_Date = db.Column(db.Date)
    Purchase_Address = db.Column(db.String(15), unique=True)
