from dataclasses import field, fields
from email.policy import default
from pyexpat import model
import string
from rest_framework import serializers

from mvp2.maze import resolveMaze
from .models import Maze
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from dataclasses import dataclass
class ExtraFieldSerializer(serializers.Serializer):
    def to_representation(self, instance): 
        # this would have the same as body as in a SerializerMethodField
        return 'my logic here'

    def to_internal_value(self, data):
        # This must return a dictionary that will be used to
        # update the caller's validation data, i.e. if the result
        # produced should just be set back into the field that this
        # serializer is set to, return the following:
        return {
          self.field_name: 'Any python object made with data: %s' % data
        }

class MazeSerializer(serializers.ModelSerializer):
    class Meta:
        # user=serializers.HiddenField(default=serializers.CurrentUserDefault())
        model=Maze
        fields=[
            'user','walls','gridsize','entrance','destination'
        ]
  

class MazeSerializerPathShort(serializers.ModelSerializer):
    class Meta:
        # user=serializers.HiddenField(default=serializers.CurrentUserDefault())
        # model_method_field = serializers.CharField(source='path')
        model=Maze
        fields=[
            'user','walls','gridsize','entrance','destination'
        ]
    def to_representation(self, instance):
      representation = super().to_representation(instance)    
      if instance.destination=='':
        x=None
      else: x=instance.destination
      short,long=resolveMaze(instance.gridsize,instance.walls,instance.entrance,x)
      short,long=resolveMaze(instance.gridsize,instance.walls,instance.entrance,None)
      p = ','.join(map(str, short))
      representation['path']=p#adding key and value 
      return representation

class MazeSerializerPathLong(serializers.ModelSerializer):
    class Meta:
        # user=serializers.HiddenField(default=serializers.CurrentUserDefault())
        # model_method_field = serializers.CharField(source='path')
        model=Maze
        fields=[
            'user','walls','gridsize','entrance','destination'
        ]
    def to_representation(self, instance):
      representation = super().to_representation(instance)
      if instance.destination=='':
        x=None
      else: x=instance.destination
      short,long=resolveMaze(instance.gridsize,instance.walls,instance.entrance,x)
      p = ','.join(map(str, long))
      representation['path']=p#adding key and value 
      return representation

class MazeSerializer2(serializers.ModelSerializer):
    # path=serializers.CharField()
    user=serializers.IntegerField()
    walls=serializers.CharField()
    gridsize=serializers.CharField()
    entrance=serializers.CharField()
    destination=serializers.CharField()
    def create(self, validated_data):
        return ReportParams(**validated_data)
@dataclass
class ReportParams:
    # path:string
    user:int
    walls:string
    gridsize:string
    entrance:string
    destination:string


def maze_report(param:ReportParams):
    data=[]
    queryset=Maze.objects.filter(user_id=param.user)
    for entry in queryset:
        walls=entry["walls"]
        data.append(walls)
    
    return data
