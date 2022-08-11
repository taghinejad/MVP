from django.test import TestCase
from vendor.models import Myuser, Product
from django.contrib.auth.models import User



    
class TestAppModels(TestCase):
    # setUp function intilize each time when testing, here it will be called twise as two function exists
    def setUp(self):
        print("test model")
        self.u=User.objects.first()

    def test_model_Product_str(self):
        p=Product.objects.create(cost=20,name="testPie",sellerid=self.u)
        print(p)
        self.assertEqual(str (p),"testPie")
    def test_model_Myuser_str(self):
        p=Myuser.objects.create(deposit=20,role="buyer",user=self.u)
        print(p)
        self.assertEqual(str (p),"buyer 20")

class TestAppModels2(TestCase):
    # setUpTestData function intilize once at first
    @classmethod
    def setUpTestData(cls):
        print("test class function setup")
        cls.u=User.objects.last()

    def test_model_Product_str(self):
        p=Product.objects.create(cost=20,name="testPie",sellerid=self.u)
        print(p)
        self.assertEqual(str (p),"testPie")
    def test_model_Myuser_str(self):
        p=Myuser.objects.create(deposit=20,role="buyer",user=self.u)
        print(p)
        self.assertEqual(str (p),"buyer 20") 
    # def test_model_deposit_post(self):
    #     us=Myuser.objects.create(role="buyer",user=self.u)
    #     print(p)
    #     self.assertEqual(str (p),"buyer 20") 