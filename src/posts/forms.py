from django.forms import ModelForm, FileInput
from posts.models import Review, Ticket


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]
        labels = {
            'headline': ("Titre de votre Review"),
            'rating': ("Note / 5"),
            'body': ("Qu'en avez-vous pensez"),
        }


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        widgets = {
            'image': FileInput(),
        }
        labels = {
            'title': ("Titre de l'oeuvre"),
            'description': ("Résumé"),
            'image': ("Couverture"),
        }
