# Generated by Django 4.1 on 2022-08-11 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0004_myuser_bought_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='role',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
