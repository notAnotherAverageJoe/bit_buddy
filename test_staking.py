import datetime
import unittest
from app import app, db, get_user_id, seed_database, bcrypt
from models import User, TransactionHistory
from flask import session
from decimal import Decimal
from flask_bcrypt import Bcrypt




#    python -m unittest -v  test_staking.py
class reset(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            seed_database()
            self.bcrypt = Bcrypt(app)
            
            db.create_all()
            self.setup_users()
            self.setup_transactions()

    def setup_users(self):
        existing_user = User.query.filter_by(id=1).first()
        if existing_user is None:
            user = User(id=1, username="testuser", email="testuser@example.com", password_hash="dummy_password_hash")
            db.session.add(user)
            db.session.commit()
        else:
            self.user_id = existing_user.id

    def setup_transactions(self):
        transaction1 = TransactionHistory(user_id=self.user_id, cryptocurrency_id=1, transaction_type='buy', amount=Decimal('0.5'))
        transaction2 = TransactionHistory(user_id=self.user_id, cryptocurrency_id=1, transaction_type='sell', amount=Decimal('1.2'))
        db.session.add(transaction1)
        db.session.add(transaction2)
        db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_money_made(self):
        response = self.app.get('/money-made')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Total amount of money your Bitcoins are worth', response.data)

    def test_calculate_staking(self):
        total_money_made = Decimal('100.00')
        response = self.app.post('/calculate-staking', data={'total_money_made': str(total_money_made)})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Staking Returns', response.data)

        # Check the calculated returns
        self.assertIn(b'30 days', response.data)
        self.assertIn(b'365 days', response.data)

    def test_transaction_history(self):
        response = self.app.get('/transaction-history')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Transaction History', response.data)
   



    def test_reset_transactions(self):
        with app.app_context():
            # Create a test user
            test_user = User(username='testuser', email='testuser@example.com')
            bcrypt = Bcrypt(app)
            test_user.password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
            db.session.add(test_user)
            db.session.commit()

            # Add transactions for the test user
            transaction1 = TransactionHistory(user_id=test_user.id, cryptocurrency_id=1, transaction_type='buy', amount=5.0)
            transaction2 = TransactionHistory(user_id=test_user.id, cryptocurrency_id=1, transaction_type='sell', amount=3.0)
            db.session.add(transaction1)
            db.session.add(transaction2)
            db.session.commit()
            
            # Simulate a login by setting the user_id in the session
            with self.app.session_transaction() as sess:
                sess['user_id'] = test_user.id
            
            # Verify the transactions exist before the reset
            transactions = TransactionHistory.query.filter_by(user_id=test_user.id).all()
            self.assertEqual(len(transactions), 2)
            
            # Make a POST request to reset transactions
            response = self.app.post('/reset-transactions')
            
            # Check if the response status code is 302 (indicating redirection)
            self.assertEqual(response.status_code, 302)  
            
            # Verify transactions associated with the test user are deleted
            transactions = TransactionHistory.query.filter_by(user_id=test_user.id).all()
            self.assertEqual(len(transactions), 0)

if __name__ == '__main__':
    unittest.main()


