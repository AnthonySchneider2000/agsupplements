# Generated by Django 4.2.4 on 2023-10-04 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_item_servings'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='units',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
