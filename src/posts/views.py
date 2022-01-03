from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from posts.forms import ReviewForm, TicketForm
from posts.models import Review, Ticket
from abonnement.models import Friendship

# Get a list of followed users ids


def get_followed_users(user_pk):
    followed_users = Friendship.objects.filter(user_id=user_pk)
    print(f"Vous suivez {followed_users}")
    followed_users_id = []
    for f_user in followed_users:
        followed_users_id.append(f_user.followed_id)

    print(f'{len(followed_users_id)} utilisateurs trouvés')
    print(followed_users_id)

    if len(followed_users_id) == 0:
        return False
    return followed_users_id


# Retrieves every Ticket made by the user passed in,
# As well as Tickets answered by the passed in user.

def get_everything_user_related(user_identifier):
    ur_tickets = Ticket.objects.filter(user_id=user_identifier)
    # Retrieve every ticket from the author, with their responses
    for user_related_ticket in ur_tickets:
        try:
            linked_review = Review.objects.get(
                ticket_id=user_related_ticket.pk)
            user_related_ticket.review = linked_review
        except Review.DoesNotExist:
            pass
            # Retrieve every review from the author, linked to their original ticket
    ur_reviews = Review.objects.filter(user_id=user_identifier)
    tickets_answered_by_user = []
    for user_related_review in ur_reviews:
        # Let's grab the original ticket user's ID to check if our user is the the author, if so, pass
        # Since it'll already be listed by the upper half of this function
        if Review.objects.get(ticket_id=user_related_review.ticket_id).user_id == user_identifier:
            pass
        else:
            # We are not the author of the Ticket, let's add it to our tickets list, no clash possible
            ticket = Ticket.objects.get(
                ticket_id=user_related_review.ticket_id)
            ticket.review = user_related_review
            ticket.append(tickets_answered_by_user)

    return [*ur_tickets, *tickets_answered_by_user]


def my_posts(request):
    # Loads our tickets & their responses.
    # Then load our responses with their tickets.
    my_articles = get_everything_user_related(request.user.pk)

    context = {}
    if len(my_articles) == 0:
        context['message'] = "Vous pourrez voir vos posts ici !"
    context['articles'] = my_articles
    return render(request, "review/my_posts.html", context)


@login_required
def list_articles(request):
    followed_users = get_followed_users(request.user.pk)
    context = {}

    #  If we don't follow anyone
    if followed_users is False:
        context['message'] = ('Vous ne suivez personne et ne verrez donc aucun post.'
                              'Rendez-vous dans la rubrique "Abonnements" pour commencer à suivre des utilisateurs !')
    else:
        tickets_to_display = Ticket.objects.filter(user_id__in=followed_users)
        for ask in tickets_to_display:
            try:
                linked_review = Review.objects.get(ticket_id=ask.pk)
                ask.review = linked_review
            except Review.DoesNotExist:
                pass
        context['articles'] = tickets_to_display
        context['articles'] = sorted(context['articles'],
                                     key=lambda post: post.time_created,
                                     reverse=True
                                     )
    # return render(request, 'feed.html', context={'posts': posts})

    return render(request, "review/list_articles.html", context)


@login_required
def write_review(request, id_article):
    # Grab the ticket we are answering to
    instance_ticket = Ticket.objects.get(
        pk=id_article)

    try:
        id_review = Review.objects.get(ticket_id=id_article)
    except Review.DoesNotExist:
        id_review = None

    if request.method == "GET":
        if id_review is None:
            message = "Ajouter"
        else:
            message = "Modifier"
        form = ReviewForm(instance=id_review)
        # Used in the HTML
        ticket = instance_ticket
        # print(ticket.image.url)
        return render(request, "review/review.html", locals())

    elif request.method == "POST":
        # Now let's check if we are answering or creating a ticket
        try:
            review_instance = Review.objects.get(ticket_id=id_article)
            form = ReviewForm(request.POST, instance=review_instance)
        except Review.DoesNotExist:
            review_instance = None
            form = ReviewForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.ticket = instance_ticket
            form.save()
        return redirect("flux")


@ login_required
def write_ticket(request, id_article=None):
    instance_article = Ticket.objects.get(
        pk=id_article) if id_article is not None else None

    if request.method == "GET":
        # Do we modify or create a new ticket ?
        if id_article is None:
            message = "Effectuer"
        else:
            message = "Modifier"

        form = TicketForm(instance=instance_article)
        return render(request, "review/write_ticket.html", locals())

    elif request.method == "POST":
        # We modify an existing article
        if id_article is not None:
            form = TicketForm(request.POST, request.FILES,
                              instance=instance_article)
        else:
            # We create a new one
            form = TicketForm(request.POST, request.FILES)

        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect("flux")


@ login_required
def create_and_resolve(request):
    # Create the HTML get with our 2 forms in 1 page
    if request.method == "GET":
        context = {'formset1': TicketForm, 'formset2': ReviewForm}
        return render(request, "review/selfresolvedticket.html", context)

    # Retrieve the 2 forms in a single POST request
    if request.method == "POST":
        rget = request.POST.get
        rget_img = request.FILES.get('image', False)
        if not rget_img:
            # We can't return the forms separately from the HTML's POST request, so
            # Create our objects manually from our retrieved data

            # No image
            instance_ticket = Ticket(title=rget("title"),
                                     description=rget("description"),
                                     user=request.user
                                     )
        else:
            # Image
            instance_ticket = Ticket(title=rget("title"),
                                     description=rget("description"),
                                     user=request.user,
                                     image=rget_img)

        instance_ticket.save()

        review = Review(ticket=instance_ticket,
                        rating=rget("rating"),
                        user=request.user,
                        headline=rget("headline"),
                        body=rget("body")
                        )
        review.save()

        return redirect("flux")


@login_required
def delete_post(request, id_article, type=0):
    if type == 1:
        DeleteType = Review.objects.get(id=id_article)
    else:
        DeleteType = Ticket.objects.get(id=id_article)

    post = DeleteType
    if request.method == "POST":
        if type == 0 and post.image is not None:
            post.image.delete()
        post.delete()
        return redirect("flux")

    context = {'item': post, 'type': type}
    return render(request, "review/delete.html", context)
