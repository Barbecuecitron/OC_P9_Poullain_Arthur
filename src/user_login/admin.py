from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from .models import User

admin.site.register(User)
