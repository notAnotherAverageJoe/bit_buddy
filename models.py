

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'testingtacos'  
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///bitbuddy"  
db = SQLAlchemy(app)
















def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
    