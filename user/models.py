from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    class Meta:
        db_table = 'my_user'

    bio = models.CharField(max_length=30, default='')
