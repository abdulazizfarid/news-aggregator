import json

from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient


class TestGetRequest(TestCase):
    @classmethod
    # def setUpTestData(cls):
    #     print("setUpTestData: Run once to set up non-modified data for all class methods.")
    #     pass
    #
    # def setUp(self):
    #
    #     factory = APIRequestFactory()
    #     request = factory.get('news/')
    #
    #     pass

    def test_getNews(self):
        response = self.client.get('news/')
        self.assertEqual(response.status_code, 200)
