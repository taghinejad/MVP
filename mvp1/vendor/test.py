from django.test import TestCase
from django.urls import reverse,resolve
from rest_framework.test import APIClient
from vendor.models import Myuser, Product
from vendor.views import DepositView, ProductModelViewSet, buy
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
#create your tests here. 

class URLTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='user01', password='123456')

    def test_homepage(self):
        response=self.client.get('/')
        self.assertEqual(response.status_code,200)

    def test_url_deposit(self):
        #checks that if the deposit urls open the deposit view
        url=reverse("deposit")
        self.assertEquals(resolve(url).func.view_class, DepositView)

    def test_url_buy(self):
        #checks that if the buy urls open the buy function 
        url=reverse("buy")
        self.assertEquals(resolve(url).func, buy)

    def test_url_get_deposit(self):
        # token = Token.objects.get(user__username='badmin')
        # user = User.objects.create(username='user01', password='123456')
        client = APIClient()
        client.force_authenticate(user=self.user)
        response=client.get('/deposit/')
        self.assertEqual(response.status_code,200)
    def test_url_post_deposit(self):
        myuser=Myuser.objects.create(user=self.user,role="buyer")
        client = APIClient()
        client.force_authenticate(user=self.user)
        response=client.post('/deposit/', {"deposit": 50}, format='json')
        self.assertEqual(response.status_code,200)

    def test_url_post_buy(self):
        # the data of user and other models are not acceable through test, so new users are created. 
        suser = User.objects.create(username='user02', password='123456')
        myuser=Myuser.objects.create(user=self.user,role="buyer",deposit=50)
        product=Product.objects.create(name="testproduct",cost=20,amountAvailable=50,sellerid=suser)
        client = APIClient()
        client.force_authenticate(user=self.user)
        response=client.post('/buy/', {"id": product.id,"amountAvailable": 1}, format='json')
        self.assertEqual(response.status_code,200)
        