from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import QueuerForm
from .models import Queuer

# Create your views here.


def application(request):
    if request.method == "POST":
        form = QueuerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                reverse("waitlist:thanks")
                + "?waitlist=%s" % Queuer.objects.last().waitlist_number
            )
    else:
        form = QueuerForm()
    return render(request, "application.html", {"form": form})
