from django.db import models
from django.contrib.auth.models import User
import os
from sublimebackup import settings
# Create your models here.
class snippet(models.Model):
    snippet_file = models.TextField()
    original_name = models.TextField()
    dropbox_id = models.TextField()
    owner = models.ForeignKey(User, null = True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.original_name} by {self.owner.username}'

class kloudless_keys(models.Model):
    name = models.TextField()
    key = models.TextField()