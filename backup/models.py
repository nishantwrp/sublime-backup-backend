from django.db import models
from django.contrib.auth.models import User
import os
from sublimebackup import settings
# Create your models here.
class snippet(models.Model):
    snippet_file = models.FileField(blank=False,null=False)
    original_name = models.TextField()
    owner = models.ForeignKey(User, null = True, on_delete=models.SET_NULL)

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.snippet_file.name))
        super(snippet,self).delete(*args,**kwargs)

    def __str__(self):
        return f'{self.original_name} by {self.owner.username}'