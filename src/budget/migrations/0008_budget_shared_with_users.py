# Generated by Django 3.2 on 2021-04-25 22:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('budget', '0007_auto_20210425_2340'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='shared_with_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
