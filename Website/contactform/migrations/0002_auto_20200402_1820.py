# Generated by Django 3.0.3 on 2020-04-02 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactform', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactform',
            name='date',
            field=models.CharField(default='', max_length=12),
        ),
        migrations.AddField(
            model_name='contactform',
            name='time',
            field=models.CharField(default='', max_length=12),
        ),
    ]
