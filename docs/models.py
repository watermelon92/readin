from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Doc(models.Model):
    name = models.CharField(max_length=15)
    fileUrl = models.CharField(max_length=200)
    fileLocation = models.CharField(max_length=200)
    last_updated = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(User,related_name='docs')

    def __str__(self):
        return self.name
