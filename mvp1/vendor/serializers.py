from dataclasses import field, fields
from email.policy import default
from pyexpat import model
from rest_framework import serializers
from .models import Myuser, Product, todo
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
class todoSerializer(serializers.ModelSerializer):
    class Meta:
        model=todo
        fields=(
            'title','complete'
        )

MIN_LEN=8

class ProductSerializerRead(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"
    

class MyuserSerializer(serializers.ModelSerializer):
    user=serializers.HiddenField(default=serializers.CurrentUserDefault())
    bought_product=ProductSerializerRead()
    class Meta:
        model=Myuser
        fields=(
            "user","deposit","role","bought_product"
        )

        def validate(self, attrs):
            print(serializers.CurrentUserDefault())
            if attrs["user"]!=serializers.CurrentUserDefault():
                raise serializers.ValidationError("User does not match.")
            return attrs

class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(
        write_only=True,
        min_length=3,
        
    )

    password2=serializers.CharField(
        write_only=True,
        min_length=3,
     
    )
    role=serializers.CharField(    
        write_only=True,  
        default="seller"
    )
    deposit=serializers.IntegerField(
        write_only=True,
        default=0
    )
    
    class Meta:
        model=User
        fields="__all__"
    
    def validate(self, attrs):
        if attrs["password"]!=attrs["password2"]:
            raise serializers.ValidationError("Password does not match.")
        return attrs

    def create(self,validated_data):
        us=User.objects.create(
            username=validated_data["username"],    
        )

        us.set_password(validated_data["password"])
        us.save()
        f=Myuser.objects.create(user=us,role=validated_data["role"],deposit=validated_data["deposit"])
        f.save()
    
        token = Token.objects.create(user=us)
        token.save()
        return us

class ProductSerializerWrite(serializers.ModelSerializer):
# we this line below, instead of using id of currency, i can use the code of the currency to create new transactions 
# and also other api like get will return the code of currency instead of the id
# therefore, everywhere, code will be used instead of id
   
    sellerid=serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model=Product
        fields=(
        "sellerid",
        "amountAvailable",
        "cost",
        "name",
        )
    
    # as category is a forighn key and every user have an id, then 
    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(instance, *args, **kwargs)
        #retrieve the user that made the request

    def validate(self, attrs):
        if attrs["cost"]!=5 and  attrs["cost"]!=10 and  attrs["cost"]!=20 and  attrs["cost"]!=50 and  attrs["cost"]!=100 :
            raise serializers.ValidationError("Cost does not match. only 5, 10, 20, 50 and 100 cent are acceptable")
        return attrs


class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=("id","username","deposit","role")
        read_onlly_fields=fields