from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import  ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework import status
from .models import Maze

from .serializers import *
# Create your views here.
class MazeView(APIView):
    def get(self,request,*args,**kwargs):
        mymaze=Maze.objects.filter(user=self.request.user)
        serializer=MazeSerializer(mymaze,many=True)
        return Response({'maze':serializer.data})

    def post(self,request,*args,**kwargs):
        request.data["user"]=self.request.user.id
        serializer=MazeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)
    
    permission_classes=(IsAuthenticated,)

@api_view(['GET'])
def maze_detailShort(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        maze = Maze.objects.get(pk=pk)
    except Maze.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        
        steps = request.GET.get('steps')
        if steps=="max":
            serializer = MazeSerializerPathLong(maze)
        else:
            serializer = MazeSerializerPathShort(maze)
        # print(serializer["data"])
        return Response(serializer.data)