from django.test import TestCase
from django.urls import reverse,resolve
from rest_framework.test import APIClient
from .models import Maze
from vendor.views import DepositView, ProductModelViewSet, buy
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
#create your tests here. 

class URLTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='user01', password='123456')

    def test_url_get_deposit(self):
        # token = Token.objects.get(user__username='badmin')
        # user = User.objects.create(username='user01', password='123456')
        client = APIClient()
        client.force_authenticate(user=self.user)
        response=client.get('/maze/')
        self.assertEqual(response.status_code,200)
    def test_url_post_maze(self):
        # maze=Maze.objects.create(user=self.user,walls="C1,G1,A2,C2,E2,G2,C3,E3,B4,C4,E4,F4,G4,B5,E5,B6,D6,E6,G6,H6,B7,D7,G7,B8",gridsize="8x8",entrance="A1")
        client = APIClient()
        client.force_authenticate(user=self.user)
        response=client.post('/maze/', {"walls": "C2,G1,A3,C2,E2,G2,C3,E3,B4,C4,E4,F4,G4,B5,E5,B6,D6,E6,G6,H6,B7,D7,G7,B8",
        "gridsize":"8x8","entrance":"A2"}, format='json')
        self.assertEqual(response.status_code,200)
    def test_url_get_shortest(self):
        maze=Maze.objects.create(user=self.user,walls="C1,G1,A2,C2,E2,G2,C3,E3,B4,C4,E4,F4,G4,B5,E5,B6,D6,E6,G6,H6,B7,D7,G7,B8",gridsize="8x8",entrance="A1")
        client = APIClient()
        client.force_authenticate(user=self.user)
        response=client.get('/maze/'+str(maze.id)+"/solution?steps=min" )
        self.assertEqual(response.status_code,200)