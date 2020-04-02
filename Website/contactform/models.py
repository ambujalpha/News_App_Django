from __future__ import unicode_literals
from django.db import models


class ContactForm(models.Model):

    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    txt = models.TextField()
    date = models.CharField(max_length=12, default="")
    time = models.CharField(max_length=12, default="")

    def __str__(self):
        return self.name




