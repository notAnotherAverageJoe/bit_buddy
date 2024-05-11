from flask import Flask, render_template
from models import connect_db, db
from flask import Flask
from models import cryptocurrency, User
from flask_cors import CORS # type: ignore



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
    return render_template("index.html")


from flask import jsonify


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







####################3333

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


# @app.route("/api/cryptocurrencies/<int:currency_id>", methods=["DELETE"])
# def remove_cryptocurrency(currency_id):
#     """Delete cryptocurrency and return confirmation message."""

#     # Query the database for the cryptocurrency with the given ID
#     cryptocurrency = cryptocurrency.query.get_or_404(currency_id)

#     # Delete the cryptocurrency from the database
#     db.session.delete(cryptocurrency)
#     db.session.commit()

#     # Return a JSON confirmation message
#     return jsonify(message="Cryptocurrency deleted")

from flask import jsonify

from flask import request, jsonify
from models import db, cryptocurrency  # Assuming the Cryptocurrency model is imported correctly

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