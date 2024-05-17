import subprocess
import bcrypt
from flask import Flask, render_template, session, redirect, url_for, flash
from crypto_api import get_bitcoin_data, get_blockchain_info
from forms import RegistrationForm
from models import TransactionHistory, connect_db, db, User
from flask import Flask
from models import cryptocurrency, User
from flask_cors import CORS # type: ignore
from decimal import ROUND_HALF_UP, Decimal
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()


app = Flask(__name__)
CORS(app)


app.config['SECRET_KEY'] = "testingtacos"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///bitbuddy"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def seed_database():
    try:
        subprocess.run(["psql", "-d", "bitbuddy", "-U", "joseph", "-f", "seed.sql"])
        print("Database seeded successfully!")
    except Exception as e:
        print("Error while seeding the database:", e)
        
connect_db(app)
# with app.app_context():
#      db.create_all()
seed_database()


@app.route("/")
def home():
    """homepage"""
    return render_template("home.html")

@app.route("/about")
def about():
    """About page"""
    return render_template("about.html")


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
            # If user exists and password is correct, set user ID as logged in
            session['user_id'] = user.id  # Store user ID in session
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to dashboard or home page
        else:
            # If user doesn't exist or password is incorrect, show error message
            flash('Invalid username or password', 'error')

    # Render the login form template
    return render_template('/users/login.html')






@app.route('/logout')
def logout():
    # Remove user_id from session to log out the user
    session.pop('user_id', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))


#=============================== ^^^^^ Login/register ^^^^^ ==========================


@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'user_id' in session:
        # Get the user ID from the session
        user_id = session['user_id']
        
        # Query the database to get the user's information
        user = User.query.get(user_id)
        
        # Check if the user exists
        if user:
            # Get the username and email from the user object
            username = user.username
            email = user.email
            
            # Render the dashboard template with the user's information
            return render_template('/users/dashboard.html', username=username, email=email)
        else:
            # If the user does not exist, log them out and redirect to the login page
            flash('User not found. Please log in again.', 'error')
            session.pop('user_id', None)
            return redirect(url_for('login'))
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


####################################----- vvvv User buy,sell,stake vvvv ----####################
def get_user_id():
    # Implement this function to retrieve the user's ID from the session
    return session.get('user_id')

@app.route('/bitcoinbuy', methods=['GET', 'POST'])
def bitcoin_buy():
    # Check if the user is logged in
    if 'user_id' not in session:
        # If not logged in, redirect to login page
        return redirect(url_for('login'))

    bitcoin_data = get_bitcoin_data()
    if bitcoin_data:
        bitcoin_price = float("{:.2f}".format(bitcoin_data['quote']['USD']['price']))
        bitcoin_symbol = bitcoin_data['symbol']
    else:
        bitcoin_price = None
        bitcoin_symbol = None

    if request.method == 'POST':
        # Handles the bitcoin buy operation
        bitcoin_amount = request.form['bitcoin_amount']
        try:
            bitcoin_amount_float = float(bitcoin_amount)
            total_cost = bitcoin_amount_float * bitcoin_price
            total_cost_formatted = "{:.2f}".format(total_cost)

            # Retrieve the current user's ID from the session
            user_id = get_user_id()

            # Query the database to find the user by user ID
            user = User.query.get(user_id)

            if user:
                # Save transaction to the database
                new_transaction = TransactionHistory(
                    user_id=user_id,
                    cryptocurrency_id=1,  # hard coded due to time limitations, left open for future coins
                    transaction_type='buy',
                    amount=bitcoin_amount_float
                )
                db.session.add(new_transaction)
                db.session.commit()

                buy_confirmation = f'Bought {bitcoin_amount} {bitcoin_symbol} at ${bitcoin_price} each. Total cost: ${total_cost_formatted}'
                return render_template('/users/bitcoin_buy.html', bitcoin_price=bitcoin_price, bitcoin_symbol=bitcoin_symbol, buy_confirmation=buy_confirmation)
            else:
                # Handle the case where the user does not exist
                return "User does not exist"
        except ValueError:
            # Handle invalid input for bitcoin_amount
            return "Invalid amount entered. Please enter a valid number."
    else:
        return render_template('/users/bitcoin_buy.html', bitcoin_price=bitcoin_price, bitcoin_symbol=bitcoin_symbol)



@app.route('/bitcoinsell', methods=['GET', 'POST'])
def bitcoin_sell():
    # Check if the user is logged in
    if 'user_id' not in session:
        # If not logged in, redirect to login page
        return redirect(url_for('login'))

    bitcoin_data = get_bitcoin_data()
    if bitcoin_data:
        bitcoin_price = float("{:.2f}".format(bitcoin_data['quote']['USD']['price']))
        bitcoin_symbol = bitcoin_data['symbol']
    else:
        bitcoin_price = None
        bitcoin_symbol = None

    if request.method == 'POST':
        # Handle sell operation
        bitcoin_amount = request.form['bitcoin_amount']
        try:
            bitcoin_amount_float = float(bitcoin_amount)
            total_earning = bitcoin_amount_float * bitcoin_price
            total_earning_formatted = "{:.2f}".format(total_earning)

            # Retrieve the current user's ID from the session
            user_id = get_user_id()

            # Query the database to find the user by user ID
            user = User.query.get(user_id)

            if user:
                # Save transaction to the database
                new_transaction = TransactionHistory(
                    user_id=user_id,
                    cryptocurrency_id=1,  # Replace with the appropriate cryptocurrency ID
                    transaction_type='sell',
                    amount=bitcoin_amount_float
                )
                db.session.add(new_transaction)
                db.session.commit()

                sell_confirmation = f'Sold {bitcoin_amount} {bitcoin_symbol} at ${bitcoin_price} each. Total earning: ${total_earning_formatted}'
                return render_template('/users/bitcoin_sell.html', bitcoin_price=bitcoin_price, bitcoin_symbol=bitcoin_symbol, sell_confirmation=sell_confirmation)
            else:
                # Handle the case where the user does not exist
                return "User does not exist"
        except ValueError:
            # Handle invalid input for bitcoin_amount
            return "Invalid amount entered. Please enter a valid number."
    else:
        return render_template('/users/bitcoin_sell.html', bitcoin_price=bitcoin_price, bitcoin_symbol=bitcoin_symbol)




@app.route('/money-made')
def money_made():
    # Function to get the current price of Bitcoin
    def get_bitcoin_price():
        bitcoin_data = get_bitcoin_data()
        if bitcoin_data:
            bitcoin_price = bitcoin_data['quote']['USD']['price']
            return bitcoin_price
        else:
            return None

    # Define a function to retrieve the current user's ID from the session
    def get_user_id():
        # Implement this function to retrieve the user's ID from the session
        return session.get('user_id')

    # Query transactions associated with the current user's ID
    transactions = TransactionHistory.query.filter_by(user_id=get_user_id()).all()

    total_money_made = 0

    # Iterate through each transaction and calculate the total value
    for transaction in transactions:
        # Get the current price of Bitcoin
        bitcoin_price = get_bitcoin_price()
        
        if bitcoin_price is not None:
            # Convert bitcoin_price to a Decimal object
            bitcoin_price_decimal = Decimal(str(bitcoin_price))

            # Get the cryptocurrency associated with the transaction
            cryptocurrency_made = cryptocurrency.query.get(transaction.cryptocurrency_id)
            
                # Now perform the multiplication
            total_value = transaction.amount * bitcoin_price_decimal
            
            total_value = Decimal(str(total_value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            # Adjust total_money_made based on transaction type
            if transaction.transaction_type == 'buy':
                total_money_made += total_value
            elif transaction.transaction_type == 'sell':
                total_money_made -= total_value

            print(f"Transaction ID: {transaction.id}, Amount: {transaction.amount}, Total Value: ${total_value:.2f}")

    return render_template('/users/bitcoin_values.html', total_money_made=total_money_made)



from flask import request

from decimal import Decimal, ROUND_HALF_UP

@app.route('/calculate-staking', methods=['POST'])
def calculate_staking():
    if request.method == 'POST':
        # Retrieve the total money made from the form data
        total_money_made = Decimal(request.form['total_money_made'])

        # Calculate staking returns for different periods at 10% interest
        interest_rate = Decimal('0.10')
        periods = [30, 60, 90, 120, 150, 175, 180, 210, 240, 270, 300, 330, 365]

        # Calculate staking returns for each period and store in a dictionary
        staking_returns = {}
        for days in periods:
            # Convert days to Decimal to ensure accurate calculations
            days_decimal = Decimal(days)

            # Calculate staking return with Decimal arithmetic
            staking_return = (total_money_made * (Decimal('1') + interest_rate) ** (days_decimal / Decimal('365'))) - total_money_made

            # Round the staking return to two decimal places
            staking_returns[days] = staking_return.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        return render_template('/users/staking_result.html', staking_returns=staking_returns)
    else:
        # Handle other HTTP methods if needed
        return "Method Not Allowed", 405



@app.route('/transaction-history')
def transaction_history():
    # Retrieve the current user's ID (you need to implement this function)
    user_id = get_user_id()

    # Query transaction history for the current user
    user_transactions = TransactionHistory.query.filter_by(user_id=user_id).all()

    return render_template('/users/transaction_history.html', transactions=user_transactions)



@app.route('/reset-transactions', methods=['POST'])
def reset_transactions():
    # Retrieve the current user's ID from the session
    user_id = session.get('user_id')

    # Delete all transactions associated with the current user
    TransactionHistory.query.filter_by(user_id=user_id).delete()

    # Commit the changes to the database
    db.session.commit()

    # Redirect the user to their dashboard or any other relevant page
    return redirect(url_for('dashboard'))




####################################----- ^^^^^ User buy,sell,stake ^^^^^ ----####################


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
    try:
        # Get the JSON data from the request
        data = request.json

        # Query the database for the cryptocurrency with the given ID
        cryptocurrency_data = cryptocurrency.query.get_or_404(currency_id)

        # Update the cryptocurrency data with the values from the request
        cryptocurrency_data.name = data.get('name', cryptocurrency_data.name)
        cryptocurrency_data.symbol = data.get('symbol', cryptocurrency_data.symbol)
        cryptocurrency_data.descriptions = data.get('descriptions', cryptocurrency_data.descriptions)

        # Commit the changes to the database
        db.session.commit()

        # Return the updated cryptocurrency data in JSON format
        return jsonify(cryptocurrency=cryptocurrency_data.to_dict()), 200
    except Exception as e:
        # Log the error
        app.logger.error(f"Error updating cryptocurrency: {e}")
        # Return an error response with status code 500
        return jsonify(error="Internal Server Error"), 500



from flask import jsonify

from flask import request, jsonify
from models import db, cryptocurrency  

@app.route("/api/cryptocurrencies/<int:currency_id>", methods=["DELETE"])
def remove_cryptocurrency(currency_id):
    """Delete cryptocurrency and return confirmation message."""

   
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


############################^^^^ Restful api for cryptocurrency above ^^^^####################

#############################vvvv Crypto mining game below vvvv #############################33

from flask import Flask, render_template, request, jsonify
import random



def generate_nonce(length):
    return ''.join(random.choices('0123456789', k=length))

def check_nonce(correct_nonce, user_nonce):
    matching_digits = sum(1 for digit1, digit2 in zip(correct_nonce, user_nonce) if digit1 == digit2)
    return matching_digits

nonce_length = 4  # Difficulty level of the mining process
correct_nonce = generate_nonce(nonce_length)
@app.route('/crypto_mining')
def whats_mining():
    return render_template('mining/crypto_mine.html')

@app.route('/game')
def game():
    return render_template('mining/mine.html', nonce_length=nonce_length)

@app.route('/mine', methods=['POST'])
def mine():
    global correct_nonce
    user_nonce = request.form['nonce']
    if len(user_nonce) != nonce_length or not user_nonce.isdigit():
        return jsonify({"error": f"Invalid input. Please enter a {nonce_length}-digit number."})

    matching_digits = check_nonce(correct_nonce, user_nonce)
    if matching_digits == nonce_length:
        correct_nonce = generate_nonce(nonce_length)  # Generate a new nonce for the next mining round
        return jsonify({"success": "Congratulations! You've successfully mined a block."})
    else:
        return jsonify({"matching_digits": matching_digits})

if __name__ == "__main__":
    app.run(debug=True)


