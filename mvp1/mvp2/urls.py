from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('',  MazeView.as_view(),name='maze'),
    path('<int:pk>/solution',  maze_detailShort,name='mazedetail'),
]