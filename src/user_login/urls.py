from django.urls import path
from user_login import views

urlpatterns = [
    path('', views.login_page, name='login'),
]
