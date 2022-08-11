from rest_framework import status

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from django.shortcuts import render,redirect
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets,fields
from rest_framework.views import APIView
from rest_framework.viewsets import  ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import MyuserSerializer, ProductSerializerRead, ProductSerializerWrite, UserSerializer, todoSerializer
from .models import Myuser, Product, todo
from django.contrib.auth.models import User
# Create your views here.
def index(request):
    t=todo.objects.all()
    return render(request, 'base.html',{"todo":t})

@require_http_methods(["POST"])
def add(request):
    title=request.POST['title']
    td=todo(title=title)
    td.save()
    return redirect("index")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy(request):
        
        myuser=Myuser.objects.filter(user=request.user).first()
        if myuser.bought_product is not None:
            return Response("You already bought, please reset",status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("id") is not None:
            p=Product.objects.get(pk=request.data.get("id"))
            if request.data.get("amountAvailable") is not None:
                amount=request.data.get("amountAvailable")
                if p.amountAvailable<amount:
                    return Response("Invalid Amount",status=status.HTTP_400_BAD_REQUEST)
                if myuser.deposit==0:
                    return Response("Can not afford deposit is zero",status=status.HTTP_400_BAD_REQUEST)
                if myuser.deposit<p.cost:
                    return Response("Can not afford",status=status.HTTP_400_BAD_REQUEST)
            myuser.deposit-=p.cost
            myuser.bought_product=p
            myuser.save()
            p.amountAvailable-=amount
            p.save()
        serializer=MyuserSerializer(myuser)

        # to od update user product
        return Response(serializer.data)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reset(request):
        myuser=Myuser.objects.filter(user=request.user).first()
        myuser.bought_product=None
        myuser.deposit=0
        myuser.save()      
        serializer=MyuserSerializer(myuser)
        return Response(serializer.data)


class DepositView(APIView):
    def get(self,request,*args,**kwargs):
        myuser=Myuser.objects.filter(user=self.request.user).first()
        print(myuser)

        serializer=MyuserSerializer(myuser)
        return Response({'user':serializer.data})

    def post(self,request,*args,**kwargs):
        myuser=Myuser.objects.filter(user=self.request.user).first()  
        if request.data.get("user") is not None: 
            if request.data["user"]!=myuser.id:
                return Response("Invalid User, you should login as the user",status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("deposit") is not None :
            if myuser.deposit>0:
                return Response("Can deposit one coin at the time",status=status.HTTP_400_BAD_REQUEST)
            myuser.deposit=request.data["deposit"]
        myuser.depositmoney()
        serializer=MyuserSerializer(myuser)
        return Response(serializer.data)
    
    permission_classes=(IsAuthenticated,)


class ProductModelViewSet(ModelViewSet):
    """
    if pagination is enabled use this in postman:  curl --location --request GET 'http://127.0.0.1:8000/rest/transactions/?page=4' 
    you can make django to prefetch by select_related to increase the speed
      queryset=Transaction.objects.select_related("currency","category","user")
    inorder to only prefetch transactions that belong the current user token, we use code below
    """
    def get_queryset(self):
        # return Product.objects.select_related("sellerid").filter(sellerid=self.request.user)
        return Product.objects.all()


    #to protect your vies, you have to add permission_classes = [IsAuthenticated|ReadOnly]
    permission_classes = [IsAuthenticated,]
     #so we can search by code below curl --location --request GET 'http://127.0.0.1:8000/rest/transactions/?search=ahmad'

    def get_serializer_class(self):
         if self.action in ("list", "retrieve"):
             return ProductSerializerRead
         return ProductSerializerWrite
    
    """
    if i do not save current user data in the serlizer, 
     the code below, makes the user of transaction saved by the id of loged in person
     def perform_create(self, serializer): 
          serializer.save(user=self.request.user)
    """
       


class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer