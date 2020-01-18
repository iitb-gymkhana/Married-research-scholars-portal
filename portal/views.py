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
        form = QueuerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                reverse("portal:thanks")
                + "?waitlist=%s" % Queuer.objects.last().waitlist_number
            )
    else:
        form = QueuerForm()
    return render(request, "apply.html", {"form": form})


@login_required
def logout(request):
    """Log out."""

    logout(request)
    return render(request, "portal/login.html", {"message": "logged out"})
