from __future__ import unicode_literals
from django.db import models


class News(models.Model):

    name = models.CharField(max_length=50)
    short_txt = models.TextField()
    body_txt = models.TextField()
    date = models.CharField(max_length=12)
    pic = models.TextField()
    writer = models.CharField(max_length=50)
    catname = models.CharField(max_length=50,default="-")
    catid = models.IntegerField(default=0)
    show = models.IntegerField(default=0)

    def __str__(self):
        return self.name




