import bcrypt
from flask import Flask, render_template, session, redirect, url_for, flash
from crypto_api import get_bitcoin_data, get_blockchain_info
from forms import RegistrationForm
from models import connect_db, db, User
from flask import Flask
from models import cryptocurrency, User
from flask_cors import CORS # type: ignore
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()



app = Flask(__name__)
CORS(app)




app.config['SECRET_KEY'] = "testingtacos"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///bitbuddy"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
# with app.app_context():
#      db.create_all()




@app.route("/")
def home():
    """homepage"""
    return render_template("home.html")




#===============================Login/register ==========================
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('/users/register.html', title='Register', form=form)


from flask import Flask, render_template, redirect, url_for, request, session, flash
from werkzeug.security import check_password_hash
from models import User
from flask_bcrypt import check_password_hash

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve username and password from the login form
        username = request.form['username']
        password = request.form['password']
        
        # Query the database to find the user by username
        user = User.query.filter_by(username=username).first()
        
        # Check if the user exists and the password is correct
        if user and check_password_hash(user.password_hash, password):
            # If user exists and password is correct, set user as logged in
            session['username'] = username  # Store username in session
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to dashboard or home page
        else:
            # If user doesn't exist or password is incorrect, show error message
            flash('Invalid username or password', 'error')

    # Render the login form template
    return render_template('/users/login.html')


@app.route('/logout')
def logout():
    # Remove username from session to log out the user
    session.pop('username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))


#=============================== ^^^^^ Login/register ^^^^^ ==========================


@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'username' in session:
        # Get the username from the session
        username = session['username']
        
        # Query the database to get the user's email
        user = User.query.filter_by(username=username).first()
        email = user.email if user else None
        
        # Render the dashboard template with the username and email
        return render_template('/users/dashboard.html', username=username, email=email)
    else:
        # If the user is not logged in, redirect to the login page
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('login'))

####################################----- vvvv market cap api calls are below vvvv ----- ###############################


@app.route('/bitcoin')
def bitcoin():
    bitcoin_data = get_bitcoin_data()
    
    if bitcoin_data:
        name = bitcoin_data['name']
        symbol = bitcoin_data['symbol']
        price_info = bitcoin_data['quote']['USD']
        price_usd = price_info['price']
        change_24h = price_info['percent_change_24h']
        market_cap = price_info['market_cap']
    else:
        # If bitcoin_data is not available, assign default values
        name = "N/A"
        symbol = "N/A"
        price_usd = "N/A"
        change_24h = "N/A"
        market_cap = "N/A"
    
    return render_template('/crypto_api/bitcoininfo.html', name=name, symbol=symbol, price_usd=price_usd, change_24h=change_24h, market_cap=market_cap)


@app.route('/blockchain')
def blockchain():
    blockchain_info = get_blockchain_info()
    
    if blockchain_info:
        block_height = blockchain_info['height']
        time = blockchain_info['time']
        block_hash = blockchain_info['hash']
    else:
        # If blockchain_info is not available, assign default values
        block_height = "N/A"
        time = "N/A"
        block_hash = "N/A"
    
    return render_template('/crypto_api/blockchaininfo.html', block_height=block_height, time=time, block_hash=block_hash)

####################################----- ^^^^ market cap api calls are above ^^^^ ----- ###############################


######################################----- vvvv  my API ROUTES are below vvvv---- ########################################
@app.route("/api")
def api():
    return render_template("index.html")

@app.route("/api/cryptocurrencies")
def list_cryptocurrencies():
    """Return all cryptocurrencies in the system.

    Returns JSON like:
        {cryptocurrencies: [{id, name, symbol, description}, ...]}
    """

    cryptocurrencies = [cryptocurrency.to_dict() for cryptocurrency in cryptocurrency.query.all()]
    return jsonify(cryptocurrencies=cryptocurrencies)

from flask import request, jsonify

from flask import request, jsonify
from models import cryptocurrency 
@app.route("/api/cryptocurrencies", methods=["POST"])
def create_cryptocurrency():
    """Add cryptocurrency and return data about the new cryptocurrency."""
    
    # Get JSON data from the request
    data = request.json

    # Create a new cryptocurrency object using the provided data
    new_cryptocurrency = cryptocurrency(
        name=data['name'],
        symbol=data['symbol'],
        descriptions=data['descriptions']
    )
    db.session.add(new_cryptocurrency)
    
    try:
        # Commit the changes to the database
        db.session.commit()

        # Return the newly created cryptocurrency data in JSON format with HTTP status 201 CREATED
        return jsonify(cryptocurrency=new_cryptocurrency.to_dict()), 201
    
    except Exception as e:
        # If an error occurs during commit, rollback changes and return an error response
        db.session.rollback()
        return jsonify(error=str(e)), 500


@app.route("/api/cryptocurrencies/<int:currency_id>")
def get_cryptocurrency(currency_id):
    """Return data on specific cryptocurrency."""
    
    # Query the database for the cryptocurrency with the given ID
    cryptocurrency_entry = cryptocurrency.query.get_or_404(currency_id)
    
    # Return the cryptocurrency data in JSON format
    return jsonify(cryptocurrency=cryptocurrency_entry.to_dict())


@app.route("/api/cryptocurrencies/<int:currency_id>", methods=["PATCH"])
def update_cryptocurrency(currency_id):
    """Update cryptocurrency from data in request. Return updated data."""

    # Get the JSON data from the request
    data = request.json

    # Query the database for the cryptocurrency with the given ID
    cryptocurrency_data = cryptocurrency.query.get_or_404(currency_id)

    # Update the cryptocurrency data with the values from the request
    cryptocurrency_data.name = data['name']
    cryptocurrency_data.symbol = data['symbol']
    cryptocurrency_data.descriptions = data['descriptions']

    # Commit the changes to the database
    db.session.commit()

    # Return the updated cryptocurrency data in JSON format
    return jsonify(cryptocurrency=cryptocurrency_data.to_dict())


from flask import jsonify

from flask import request, jsonify
from models import db, cryptocurrency  

@app.route("/api/cryptocurrencies/<int:currency_id>", methods=["DELETE"])
def remove_cryptocurrency(currency_id):
    """Delete cryptocurrency and return confirmation message."""

    # try:
        # Print or log the parameter value to verify it
    print("Cryptocurrency ID:", currency_id)

        # Query the database for the cryptocurrency with the given ID
    cryptocurrency_delete = cryptocurrency.query.get_or_404(currency_id)

        # Log the generated SQL query
    print("SQL Query:", db.session.query(cryptocurrency).filter_by(id=currency_id).statement)

        # Delete the cryptocurrency from the database
    db.session.delete(cryptocurrency_delete)
    db.session.commit()

        # Return a JSON confirmation message
    return jsonify(message="Cryptocurrency deleted")

    # except Exception as e:
    #     # If an error occurs, rollback changes and return an error response
    #     db.session.rollback()
    #     return jsonify(error=str(e)), 500


if __name__ == "__main__":
    app.run(debug=True)