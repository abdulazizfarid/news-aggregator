import unittest
from django.test import Client


class FavoriteTestCase(unittest.TestCase):
    def test_toggleFavorite(self):
        client = Client()
        username = "AbdulAziz"
        id = "81f94422-fa34-45b4-ab95-35edd384507e"
        response = client.post(f'http://127.0.0.1:8000/api/news/favorite?username={username}&id={id}')
        self.assertEqual(response.status_code, 200)

    def test_getFavorites(self):
        client = Client()
        username = "AbdulAziz"
        response = client.get(f'http://127.0.0.1:8000/api/news/favorite?username={username}')
        self.assertEqual(response.status_code, 200)

    def test_invalidParams(self):
        client = Client()
        username = "AbdulAziz"
        id = "81f94422-fa34-45b4-ab95-35edd384507e"
        response = client.get(f'http://127.0.0.1:8000/api/news/favorite?username={username}&id={id}')
        print(response.status_code)
        self.assertFalse(response.status_code, 200)

    def test_missingParams(self):
        client = Client()
        username = "AbdulAziz"
        response = client.get(f'http://127.0.0.1:8000/api/news/favorite?username={username}')
        print(response.status_code)
        self.assertFalse(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
