from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import QueuerForm, ApplicantForm, UndertakingForm
from .models import Queuer, Applicant


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
        # form = QueuerForm(POST, request.FILES)
        form = ApplicantForm(POST, request.FILES)
        form2 = UndertakingForm(POST)
        # TODO: can't sent in POST requests when fields are disabled,.

        if form.is_valid():
            form.save()
            form2.save()
            return redirect(reverse("portal:thanks"))
    else:
        # form = QueuerForm(
        #     initial={
        #         "name": request.user.first_name + " " + request.user.last_name,
        #         "roll_number": request.user.username,
        #         "email": request.user.email,
        #     }
        # )
        form = ApplicantForm(
            initial={
                'name': request.user.first_name + ' ' + request.user.last_name,
                'roll_no': request.user.username,
                'email': request.user.email
            }
        )
        form2 = UndertakingForm()
    return render(request, "portal/apply.html", {"form": form, 'form2': form2})


@login_required
def waitlist(request):
    user_roll_number = request.user.username
    queues = Queuer.objects.filter(roll_number=user_roll_number)
    waiting = {}
    for queue in queues:
        waiting["Type - 1"] = queue.waitlist_Type1
        waiting['Tulsi'] = queue.waitlist_Tulsi
        waiting['MRSB'] = queue.waitlist_MRSB
    return render(request, "portal/waitlist.html", {"waitlist": waiting})


@login_required
def logout(request):
    """Log out."""

    logout(request)
    return render(request, "portal/logout.html",)
