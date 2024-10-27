from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Currency

class CurrencyTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.currency_data = {
            "code": "USD",
            "name": "US Dollar",
            "symbol": "$"
        }
        self.currency = Currency.objects.create(**self.currency_data)

    def test_create_currency(self):
        response = self.client.post(reverse('currency-list-create'), {
            "code": "EUR",
            "name": "Euro",
            "symbol": "€"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_currency(self):
        response = self.client.get(reverse('currency-detail-update-delete', kwargs={'code': 'USD'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["code"], self.currency_data["code"])

    def test_update_currency(self):
        updated_data = {
            "code": "USD",
            "name": "United States Dollar",
            "symbol": "$"
        }
        response = self.client.put(reverse('currency-detail-update-delete', kwargs={'code': 'USD'}), updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], updated_data["name"])

    def test_delete_currency(self):
        response = self.client.delete(reverse('currency-detail-update-delete', kwargs={'code': 'USD'}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_currency_rate_fetch(self):
        response = self.client.get(reverse('currency-rates') + '?source_currency=USD&target_currency=EUR')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_currency_conversion(self):
        response = self.client.get(reverse('currency-convert') + '?source_currency=USD&target_currency=EUR&amount=100')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
