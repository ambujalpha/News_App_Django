# Generated by Django 3.0.3 on 2020-03-22 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cat',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
