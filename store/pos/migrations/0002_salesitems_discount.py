# Generated by Django 5.1.7 on 2025-03-20 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesitems',
            name='discount',
            field=models.FloatField(default=0),
        ),
    ]
