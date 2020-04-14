from __future__ import unicode_literals
from django.db import models


class Blacklist(models.Model):

    ip = models.CharField(max_length=10)

    def __str__(self):
        return self.ip
