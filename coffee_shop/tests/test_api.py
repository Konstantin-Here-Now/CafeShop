from rest_framework.test import APITestCase
from django.urls import reverse
from coffee_shop.models import Coffee
from coffee_shop.serializers import CoffeeSerializer
from rest_framework import status


class CoffeeAPITestCase(APITestCase):
    def test_get_list(self):
        coffee_1 = Coffee.objects.create(name='Капучино', price=125)
        coffee_2 = Coffee.objects.create(name='Кофе', price=150)

        responce = self.client.get(reverse('coffee_api_list'))

        serial_data = CoffeeSerializer([coffee_1, coffee_2], many=True).data
        serial_data = {'coffee_list': serial_data}

        self.assertEqual(status.HTTP_200_OK, responce.status_code)
        self.assertEqual(serial_data, responce.data)
