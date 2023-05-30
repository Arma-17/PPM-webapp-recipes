from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False)

    def __str__(self):
        return self.username