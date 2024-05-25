from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'testingtacos'  
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://joseph:9k4o7SJ4DbwybATEzPqnkjzI5fJkLTmd@dpg-cp8cd48l6cac73c2f7l0-a/bitbuddy"
db = SQLAlchemy(app)



class User(db.Model):
    __tablename__ = "User"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class cryptocurrency(db.Model):
    __tablename__ = 'cryptocurrency'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    descriptions = db.Column(db.String(255), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'symbol': self.symbol,
            'descriptions': self.descriptions
        }
        

        
class TransactionHistory(db.Model):
    __tablename__ = 'transactionhistory'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    cryptocurrency_id = db.Column(db.Integer, db.ForeignKey('cryptocurrency.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Numeric(18, 8), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    user = db.relationship('User', backref='transactions')
    cryptocurrency = db.relationship('cryptocurrency', backref='transactions')



def connect_db(app):
    
    """Connect this database to provided Flask app.
    """

    db.app = app
    db.init_app(app)
    