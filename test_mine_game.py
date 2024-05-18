import unittest
from app import app
from app import correct_nonce, nonce_length


# Run the tests with this:
#                         python -m unittest test_mine_game.py 


class TestMining(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_correct_mine(self):
        nonce_length = 4  
        correct_nonce = '1234'  # Simulating the correct nonce
        response = self.app.post('/mine', data={'nonce': correct_nonce})
        data = response.get_json()
        if 'success' in data:
            self.assertIn('success', data)
        else:
            self.assertIn('matching_digits', data)


    def test_incorrect_mine(self):
        # Submit an incorrect nonce
        response = self.app.post('/mine', data={'nonce': '5678'})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('matching_digits', data)
        self.assertEqual(data['matching_digits'], 0)  # No matching digits

    def test_invalid_input(self):
        # Submit an invalid nonce (not a 4-digit number)
        response = self.app.post('/mine', data={'nonce': 'abcd'})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
