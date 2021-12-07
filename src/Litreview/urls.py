"""Litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
import user_login.views
# import abonnement.urls
# import posts.urls
urlpatterns = [
    path('admin/', admin.site.urls),
    # Pour ajouter une liste d'URLS d'une app, suivre le chemin
    # Suivant :
    # path('user_login', include("user_login.urls")),
    path('', user_login.views.login_page, name='login'),
    path('logout/', user_login.views.logout_user, name='logout'),
    # path("", include('home.urls')),
    path('signup/', user_login.views.signup_page, name='signup'),
    # path('my_posts/', include('my_posts.urls')),
    path("abonnement/", include("abonnement.urls")),
    path("flux/", include("posts.urls")),
    path("posts/", include("posts.urls"))
]
