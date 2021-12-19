from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):

    CREATOR = "CREATOR"
    SUBSCRIBER = "SUBSCRIBER"

    ROLE_CHOICES = (
        (CREATOR, 'CREATOR'),
        (SUBSCRIBER, 'Subscriber'),
    )

    avatar = models.ImageField()
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
