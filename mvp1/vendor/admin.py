from django.contrib import admin
from .models import Myuser, Product, todo
# Register your models here.

admin.site.register(todo)
admin.site.register(Myuser)
admin.site.register(Product)

