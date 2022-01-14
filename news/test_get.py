import unittest
from django.test import Client


class MyTestCase(unittest.TestCase):

    def test_getNews(self):
        client = Client()
        response = client.get('http://127.0.0.1:8000/api/news/')
        self.assertEqual(response.status_code, 200)

    def test_getSearchNews(self):
        client = Client()
        query = "Random"
        response = client.get(f'http://127.0.0.1:8000/api/news/?query={query}')
        self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
    unittest.main()
