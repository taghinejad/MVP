# Generated by Django 4.1 on 2022-08-11 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp2', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maze',
            name='destination',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
