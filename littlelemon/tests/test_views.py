from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from restaurant.models import Menu
from restaurant.serializers import MenuSerializer


class MenuViewTest(APITestCase):
    def setUp(self):
        self.menu_item1 = Menu.objects.create(title='Pizza', price=12.99, inventory=5)
        self.menu_item2 = Menu.objects.create(title='Burger', price=8.99, inventory=10)

    def test_getall(self):
        response = self.client.get(reverse('menu-items'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        menu_items = Menu.objects.all()
        self.assertEqual(response.data, MenuSerializer(menu_items, many=True).data)
