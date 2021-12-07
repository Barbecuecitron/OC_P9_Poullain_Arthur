from django.db import models
from django.conf import settings  # new
#from django.contrib.auth import get_user_model
from django.db.models.fields import PositiveSmallIntegerField
#from django.core.exceptions import ValidationError
from django.core import validators
from django.db.models.fields.files import ImageField

#from posts.forms import TicketForm
#from user_login.models import User
# Create your models here.

# edit_date = models.DateTimeField(auto_now=True)


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    ticket = 0
    rating = PositiveSmallIntegerField(
        max_length=1024, validators=[validators.MinValueValidator(0),
                                     validators.MaxValueValidator(5)])
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE, default=0)
