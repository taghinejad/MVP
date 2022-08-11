from django.forms import  ValidationError
from django.db import models
from django.contrib.auth.models import User
from .maze import resolveMaze
# Create your models here.
class Maze(models.Model):
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.PROTECT)
    walls=models.CharField(max_length=1000)
    gridsize=models.CharField(max_length=20)
    entrance=models.CharField(max_length=20)
    destination=models.CharField(max_length=20,null=True,blank=True)
    def __str__(self) -> str:
        return str(self.user)+ " grid:"+str(self.gridsize)+ " entrance:"+str(self.entrance)