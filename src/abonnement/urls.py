from django.urls import path
# from my_posts.views import show_profile
from .views import open_abonnement_page, unsubscribe

urlpatterns = [
    path("", open_abonnement_page, name="abonnement"),
    path("unsubscribe/<int:user_to_unfollow_id>/",
         unsubscribe, name="unsubscribe"),
]
