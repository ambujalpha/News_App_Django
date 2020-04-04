from __future__ import unicode_literals
from django.db import models


class Trending(models.Model):

    txt = models.CharField(max_length=50)

    def __str__(self):
        return self.txt
