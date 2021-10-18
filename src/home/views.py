from django.contrib.auth import login
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


@login_required
def homepage(request):
    # return HttpResponse("<h1>Le Exemple</h1>")
    user = request.user
    User = get_user_model()
  #  users = User.objects.all().values()
    print(User.objects.all())
    infos = {'nom': user.username, 'addresse': user.email}
    return render(request, "home/index.html", infos)
