from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from django.conf import settings
from django.db import connection


class RegionPortPriceAPITestCase(TestCase):
    def setUp(self):
        # Print the database connection details
        print(f"Using database: {settings.DATABASES['default']['NAME']}")

    def test_region_existence(self):
        # Test if a specific region exists in the database via the API
        url = reverse('average_price')
        response = self.client.get(url, {
            'date_from': '2016-01-01',
            'date_to': '2016-01-10',
            'origin': 'china_main',
            'destination': 'BEZEE'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data, "Region 'china_main' does not exist.")

    def test_average_price_with_less_than_three_prices(self):
        # Test to ensure that when there are fewer than 3 prices, the result is None via the API
        url = reverse('average_price')
        response = self.client.get(url, {
            'date_from': '2016-01-04',
            'date_to': '2016-01-04',
            'origin': 'CNSGH',
            'destination': 'north_europe_main'
        })

        expected_data = [
            {"day": "2016-01-04", "average_price": None},  # Expect None if fewer than 3 prices exist
        ]
        print("dönen değer2", response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_data)
