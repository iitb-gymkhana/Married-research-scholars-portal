from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import QueuerForm
from .models import Queuer

# Create your views here.


@login_required
def portal(request):
    return render(request, "portal/home.html")


@login_required
def apply(request):
    if request.method == "POST":
        POST = request.POST
        # POST = request.POST.copy()
        # POST['roll_number'] = request.user.username
        # POST['name'] = request.user.first_name + request.user.last_name
        # POST['email'] = request.user.email
        form = QueuerForm(POST)
        # TODO: can't sent in POST requests when fields are disabled,.

        if form.is_valid():
            form.save()
            return redirect(
                reverse("portal:thanks")
                + "?waitlist=%s" % Queuer.objects.last().waitlist_number
            )
    else:
        form = QueuerForm(
            initial={
                "name": request.user.first_name + " " + request.user.last_name,
                "roll_number": request.user.username,
                "email": request.user.email,
            }
        )
    return render(request, "portal/apply.html", {"form": form})


def waitlist(request):
    user_roll_number = request.user.username
    queues = Queuer.objects.filter(roll_number=user_roll_number)
    waiting = {}
    for queue in queues:
        waiting[queue.building_applied.name] = queue.current_waitlist
    return render(request, "portal/waitlist.html", {"waitlist": waiting})


@login_required
def logout(request):
    """Log out."""

    logout(request)
    return render(request, "portal/login.html", {"message": "logged out"})
