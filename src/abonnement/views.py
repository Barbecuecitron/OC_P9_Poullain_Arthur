from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from user_login.models import User
from abonnement.forms import FollowForm
from abonnement.models import Friendship


def are_we_following(local_user_id, followed_user_id):
    is_this_guy_already_a_friend = Friendship.objects.filter(
        user_id=local_user_id).filter(followed_id=followed_user_id)
    if is_this_guy_already_a_friend.count() > 0:
        return True
    return False


@login_required
def open_abonnement_page(request):
    # Since we retrieve db objects, lets turn them into actual users
    # Before doing any interaction
    current_user = request.user
    # Our followed users objects
    followed_objects = Friendship.objects.filter(
        user_id=current_user)
    # "     " unfollowed
    followers_objects = Friendship.objects.filter(followed_id=current_user)

    followed = []
    for profile in followed_objects:
        profile_user = User.objects.get(pk=profile.followed_id)
        followed.append(profile_user)

    # Get all of our users
    all_users = User.objects.exclude(pk=current_user.id)
    unfollowed_users = []
    # Check if the user is in our friendlist
    for uf_user in all_users:
        if are_we_following(current_user.id, uf_user.id):
            pass
        else:
            unfollowed_users.append(uf_user)
    # Get our followers
    followers = []
    for follower in followers_objects:
        follower_user = User.objects.get(pk=follower.user_id)
        followers.append(follower_user)

    context = {'followed': followed,
               "unfollowed": unfollowed_users,
               "message": "",
               "followers": followers,
               "form": FollowForm}

    if request.method == "GET":
        return render(request, "abonnement/page_abonnement.html", context)
    else:
        print(request.POST)
        form = FollowForm(request.POST)

        if form.is_valid():
            followed = form.cleaned_data['follow']
            try:
                # Does the user exist in db ?
                new_to_follow = User.objects.get(
                    username=followed)
            except User.DoesNotExist:
                new_to_follow = None

            if new_to_follow is not None:

                # We can't follow ourself
                if new_to_follow == request.user:
                    context["message"] = "Vous ne pouvez pas vous suivre vous-même."
                    return render(request, "abonnement/page_abonnement.html", context)

                # We can't follow someone that we already follow
                is_this_guy_already_a_friend = Friendship.objects.filter(
                    user_id=request.user).filter(followed_id=new_to_follow)
                if is_this_guy_already_a_friend.count() > 0:
                    context["message"] = f"Vous suivez dèja {new_to_follow.username} !"
                    return render(request, "abonnement/page_abonnement.html", context)

                # Create the friendship
                friend = Friendship(user=request.user,
                                    followed=new_to_follow)
                friend.save()
                context["message"] = f"Vous suivez désormais {new_to_follow.username}."
                return redirect("abonnement")
            else:
                context["message"] = "Cet utilisateur n'existe pas."
    return render(request, "abonnement/page_abonnement.html", context)


@login_required
def unsubscribe(request, user_to_unfollow_id):
    if request.method == "GET":
        print(f"Vous voulez arrêter de suivre {user_to_unfollow_id}")
        try:
            Friendship.objects.filter(followed_id=user_to_unfollow_id).filter(
                user_id=request.user).delete()
        except Friendship.DoesNotExist:
            pass
    return redirect("abonnement")
