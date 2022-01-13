import unittest
from django.test.client import RequestFactory

from news.views import NewsView


class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('news/')

        # Test my_view() as if it were deployed at /customer/details
        response = NewsView.as_view(request)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
