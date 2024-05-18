import unittest
from app import app, db, seed_database
from models import User, TransactionHistory
from flask import session
from unittest.mock import patch
from decimal import Decimal


# How to run the test  -> python -m unittest -v test_bitcoin_routes.py

app.config['SECRET_KEY'] = "testingtacos"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///bitbuddy_test"  # Use a test database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class TestBitcoinRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            seed_database()  
            # Creating a test user
            self.test_user = User(username='testuser', email='testuser@example.com', password_hash='hashedpassword')
            db.session.add(self.test_user)
            db.session.commit()
            self.test_user_id = self.test_user.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    @patch('app.get_bitcoin_data')
    def test_bitcoin_buy_get(self, mock_get_bitcoin_data):
        mock_get_bitcoin_data.return_value = {
            'quote': {'USD': {'price': 50000.00}},
            'symbol': 'BTC'
        }
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = self.test_user_id
            
            response = client.get('/bitcoinbuy')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Current Bitcoin Price: $50000.0', response.data)  
            self.assertIn(b'Buy Bitcoin', response.data)

    @patch('app.get_bitcoin_data')
    def test_bitcoin_buy_post(self, mock_get_bitcoin_data):
        mock_get_bitcoin_data.return_value = {
            'quote': {'USD': {'price': 50000.00}},
            'symbol': 'BTC'
        }
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = self.test_user_id
            
            response = client.post('/bitcoinbuy', data={'bitcoin_amount': '0.1'})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Bought 0.1 BTC at $50000.0 each. Total cost: $5000.0', response.data)  # Adjusted text

            transaction = TransactionHistory.query.filter_by(user_id=self.test_user_id, transaction_type='buy').first()
            self.assertIsNotNone(transaction)
            self.assertEqual(transaction.amount, Decimal('0.1'))

    @patch('app.get_bitcoin_data')
    def test_bitcoin_buy_post_invalid_amount(self, mock_get_bitcoin_data):
        mock_get_bitcoin_data.return_value = {
            'quote': {'USD': {'price': 50000.00}},
            'symbol': 'BTC'
        }
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = self.test_user_id
            
            response = client.post('/bitcoinbuy', data={'bitcoin_amount': 'invalid'})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Invalid amount entered. Please enter a valid number.', response.data)

    @patch('app.get_bitcoin_data')
    def test_bitcoin_sell_get(self, mock_get_bitcoin_data):
        mock_get_bitcoin_data.return_value = {
            'quote': {'USD': {'price': 50000.00}},
            'symbol': 'BTC'
        }
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = self.test_user_id
            
            response = client.get('/bitcoinsell')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Current Bitcoin Price: $50000.0', response.data)  # Adjusted text
            self.assertIn(b'Sell Bitcoin', response.data)

    @patch('app.get_bitcoin_data')
    def test_bitcoin_sell_post(self, mock_get_bitcoin_data):
        mock_get_bitcoin_data.return_value = {
            'quote': {'USD': {'price': 50000.00}},
            'symbol': 'BTC'
        }
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = self.test_user_id
            
            response = client.post('/bitcoinsell', data={'bitcoin_amount': '0.1'})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Sold 0.1 BTC at $50000.0 each. Total earning: $5000.0', response.data)  # Adjusted text

            transaction = TransactionHistory.query.filter_by(user_id=self.test_user_id, transaction_type='sell').first()
            self.assertIsNotNone(transaction)
            self.assertEqual(transaction.amount, Decimal('0.1'))

    @patch('app.get_bitcoin_data')
    def test_bitcoin_sell_post_invalid_amount(self, mock_get_bitcoin_data):
        mock_get_bitcoin_data.return_value = {
            'quote': {'USD': {'price': 50000.00}},
            'symbol': 'BTC'
        }
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = self.test_user_id
            
            response = client.post('/bitcoinsell', data={'bitcoin_amount': 'invalid'})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Invalid amount entered. Please enter a valid number.', response.data)

if __name__ == '__main__':
    unittest.main()

