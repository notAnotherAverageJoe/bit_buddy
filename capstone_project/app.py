
from flask import Flask
from models import db, connect_db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///bitbuddy"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'testingtacos'



connect_db(app)
with app.app_context():
     db.create_all()