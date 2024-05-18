import unittest
from app import app,seed_database
from models import cryptocurrency, db


#   python -m unittest -v test_restful_api.py

app.config['SECRET_KEY'] = "testingtacos"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///bitbuddy"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
seed_database()
class TestCryptocurrencyAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_update_cryptocurrency(self):
        # Create a cryptocurrency
        response = self.app.post("/api/cryptocurrencies", json={
            "name": "Ethereum",
            "symbol": "ETH",
            "descriptions": "smart contracts"
        })
        data = response.json
        ethereum_id = data['cryptocurrency']['id']

        # Update the cryptocurrency
        response = self.app.patch(f"/api/cryptocurrencies/{ethereum_id}", json={
            "name": "Ethereum",
            "symbol": "ETH",
            "descriptions": "Smart contracts and decentralized applications"
        })

        # Assertions
        self.assertEqual(response.status_code, 200)
        updated_data = response.json
        self.assertEqual(updated_data['cryptocurrency']['name'], "Ethereum")
        self.assertEqual(updated_data['cryptocurrency']['symbol'], "ETH")
        self.assertEqual(updated_data['cryptocurrency']['descriptions'], "Smart contracts and decentralized applications")

    def test_list_cryptocurrencies(self):
        with app.app_context():
            # Add some test cryptocurrencies
            bitcoin = cryptocurrency(name="Bitcoin", symbol="BTC", descriptions="Decentralized digital currency")
            ethereum = cryptocurrency(name="Ethereum", symbol="ETH", descriptions="Blockchain platform")
            db.session.add_all([bitcoin, ethereum])
            db.session.commit()

        # Send a GET request to list cryptocurrencies
        with app.app_context():
            response = self.app.get("/api/cryptocurrencies")
            data = response.get_json()

        # Check if the response contains the expected cryptocurrencies
        self.assertEqual(response.status_code, 200)
        self.assertIn("cryptocurrencies", data)
        self.assertEqual(len(data["cryptocurrencies"]), 2)

    def test_create_cryptocurrency(self):
        # Send a POST request to create a new cryptocurrency
        with app.app_context():
            response = self.app.post("/api/cryptocurrencies", json={
                "name": "Litecoin",
                "symbol": "LTC",
                "descriptions": "Peer-to-peer cryptocurrency"
            })
        data = response.get_json()

        # Check if the response contains the newly created cryptocurrency data
        self.assertEqual(response.status_code, 201)
        self.assertIn("cryptocurrency", data)
        self.assertEqual(data["cryptocurrency"]["name"], "Litecoin")

    def test_get_cryptocurrency(self):
        with app.app_context():
            # Add a test cryptocurrency
            bitcoin = cryptocurrency(name="Bitcoin", symbol="BTC", descriptions="Decentralized digital currency")
            db.session.add(bitcoin)
            db.session.commit()

        # Send a GET request to retrieve the test cryptocurrency
            response = self.app.get(f"/api/cryptocurrencies/{bitcoin.id}")
            data = response.get_json()

            # Check if the response contains the expected cryptocurrency data
            self.assertEqual(response.status_code, 200)
            self.assertIn("cryptocurrency", data)
            self.assertEqual(data["cryptocurrency"]["name"], "Bitcoin")

    def test_update_cryptocurrency(self):
        with app.app_context():
        # Add a test cryptocurrency
            ethereum = cryptocurrency(name="Ethereum", symbol="ETH", descriptions="Blockchain platform")
            db.session.add(ethereum)
            db.session.commit()

            # Send a PATCH request to update the test cryptocurrency
            response = self.app.patch(f"/api/cryptocurrencies/{ethereum.id}", json={
                "name": "Ethereum 2.0"
            })
            data = response.get_json()

            # Check if the response contains the updated cryptocurrency data
            self.assertEqual(response.status_code, 200)
            self.assertIn("cryptocurrency", data)
            self.assertEqual(data["cryptocurrency"]["name"], "Ethereum 2.0")

    def test_remove_cryptocurrency(self):
        # Add a test cryptocurrency
        with app.app_context():
            dogecoin = cryptocurrency(name="Dogecoin", symbol="DOGE", descriptions="Meme coin")
            db.session.add(dogecoin)
            db.session.commit()

        # Send a DELETE request to remove the test cryptocurrency
            response = self.app.delete(f"/api/cryptocurrencies/{dogecoin.id}")
            data = response.get_json()

            # Check if the response contains the confirmation message
            self.assertEqual(response.status_code, 200)
            self.assertIn("message", data)
            self.assertEqual(data["message"], "Cryptocurrency deleted")

if __name__ == '__main__':
    # Run the tests
    unittest.main()

    # After tests have run, reseed the database
    
