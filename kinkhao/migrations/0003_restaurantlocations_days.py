# Generated by Django 4.0.3 on 2022-04-18 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kinkhao', '0002_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurantlocations',
            name='days',
            field=models.ManyToManyField(to='kinkhao.days'),
        ),
    ]
