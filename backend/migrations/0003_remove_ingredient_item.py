# Generated by Django 4.2.4 on 2023-09-16 04:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_ingredient_itemingredient_itemwithingredients_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='item',
        ),
    ]
