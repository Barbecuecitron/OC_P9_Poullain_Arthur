
from django.urls.conf import path
from posts.views import list_articles, write_review, write_ticket, delete_post, create_and_resolve, my_posts

urlpatterns = [
    path('', list_articles, name="flux"),
    path('write/', write_review, name="write_review"),
    path('write/<int:id_article>/',
         write_review, name="write_review"),
    path("ask/", write_ticket, name="write_ticket"),
    path("ask/<int:id_article>/", write_ticket, name="write_ticket"),
    path("delete_post/<int:id_article>/<int:type>",
         delete_post, name="delete_post"),
    path('self_resolved/',
         create_and_resolve, name="self_resolved"),
    path("my_posts/", my_posts, name="my_posts")
]
