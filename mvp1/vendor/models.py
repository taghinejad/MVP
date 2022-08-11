
from django.forms import  ValidationError
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class todo(models.Model):
    title=models.CharField(max_length=500)
    complete=models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

class Product(models.Model):
    sellerid=models.ForeignKey(User,null=True,blank=True,on_delete=models.PROTECT)
    amountAvailable=models.BigIntegerField(default=0)
    cost=models.BigIntegerField()
    name=models.CharField(max_length=200)

    def __str__(self) -> str:
        return str(self.name)
    # def save(self,*args, **kwargs):
    #     if self.amountAvailable<0:
    #         raise ValidationError("Can not be less than zero")
    #     return super().save(self,*args, **kwargs);


class Myuser(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    deposit=models.BigIntegerField(default=0)
    role=models.CharField(null=True,max_length=200,blank=True)
    bought_product=models.ForeignKey(Product,null=True,blank=True,on_delete=models.PROTECT)
    def __str__(self) -> str:
        return str(self.role)+' '+str(self.deposit)

    def depositmoney(self,*args, **kwargs):
        if self.deposit>0:
            if self.deposit!=5 and self.deposit!=10 and self.deposit!=20 and self.deposit!=50:  
                raise ValidationError("Can not be except 5,10,20,50")
        super().save(*args, **kwargs)
    


