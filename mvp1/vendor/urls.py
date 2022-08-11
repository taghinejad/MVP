from unicodedata import name
from django import views
from django.contrib import admin
from django.urls import path,include
from vendor.views import add, index,UserViewSet
from .views import  DepositView, reset,ProductModelViewSet, buy
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authtoken import views as av
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("user",UserViewSet)

router.register(r'product',ProductModelViewSet,basename='product')
urlpatterns = [
    path('', index,name="index"),
    path('add/', add,name="add"),
    path('deposit/',DepositView.as_view(),name="deposit"),
    path('buy/',buy,name="buy"),
    path('reset/',reset,name="reset"),
    path('api/token/',obtain_auth_token,name='obtain'),
    path('api-auth/', include('rest_framework.urls')),
    path('login/',av.obtain_auth_token,name="obtain-token-auth"),
]
urlpatterns+=router.urls
