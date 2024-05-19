import unittest
from app import app

#    python -m unittest test_coinmarket_api.py

class TestCryptoAPI(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_bitcoin_route(self):
        response = self.app.get('/bitcoin')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bitcoin Information', response.data)  
        
    def test_blockchain_route(self):
        response = self.app.get('/blockchain')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Blockchain Information', response.data)  

if __name__ == '__main__':
    unittest.main()
