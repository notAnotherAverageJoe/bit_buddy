import unittest
from app import app, db, seed_database, bcrypt
from models import User
from flask import session

class AuthTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db.create_all()
            seed_database()
            self.bcrypt = bcrypt
            self.setup_users()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def setup_users(self):
        with app.app_context():
            existing_user = User.query.filter_by(username="testuser").first()
            if existing_user is None:
                hashed_password = self.bcrypt.generate_password_hash('password').decode('utf-8')
                user = User(username="testuser", email="testuser@example.com", password_hash=hashed_password)
                db.session.add(user)
                db.session.commit()
                self.user_id = user.id
            else:
                self.user_id = existing_user.id

    def test_successful_login(self):
        response = self.app.post('/login', data=dict(
            username='testuser',
            password='password'
        ), follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        # Check for content that indicates a successful login
        self.assertIn(b'Welcome to the Dashboard, testuser', response.data)
        with self.app.session_transaction() as sess:
            self.assertEqual(sess['user_id'], self.user_id)

    def test_failed_login(self):
        response = self.app.post('/login', data=dict(
            username='testuser',
            password='wrongpassword'
        ), follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)
        with self.app.session_transaction() as sess:
            self.assertNotIn('user_id', sess)

    def test_logout(self):
        with self.app.session_transaction() as sess:
            sess['user_id'] = self.user_id
        
        response = self.app.get('/logout', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out', response.data)
        with self.app.session_transaction() as sess:
            self.assertNotIn('user_id', sess)


    def test_failed_registration_existing_username(self):
        response = self.app.post('/register', data=dict(
            username='testuser',
            email='newemail@example.com',
            password='password',
            confirm='password'
        ), follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'That username is taken. Please choose a different one.', response.data)

    def test_failed_registration_existing_email(self):
        response = self.app.post('/register', data=dict(
            username='newuser',
            email='testuser@example.com',
            password='password',
            confirm='password'
        ), follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'That email is taken. Please choose a different one.', response.data)

if __name__ == '__main__':
    unittest.main()
