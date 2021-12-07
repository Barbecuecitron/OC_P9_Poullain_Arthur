from django.forms import ModelForm
from posts.models import Review, Ticket


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
