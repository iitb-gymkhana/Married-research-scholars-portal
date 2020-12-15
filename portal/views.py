from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.forms.models import inlineformset_factory
import logging
from .forms import ApplicantForm, OccupyingForm, VacatingForm
from .models import Applicant
from .utils import *
import datetime

logger = logging.getLogger(__name__)

@login_required
def portal(request):
    return render(request, "portal/home.html")


@login_required
def apply(request):
    filter = ['spouse_name', 'spouse_roll_number', 'spouse_designation']
    filled = False
    if request.method == "POST":
        POST = request.POST
        form = ApplicantForm(POST, request.FILES)
        # TODO: can't sent in POST requests when fields are disabled,.
        if form.is_valid():
            form.save()
            return redirect(reverse("portal:thanks"))
    else:
        form = ApplicantForm(
            initial={
                'name': request.user.first_name + ' ' + request.user.last_name,
                'roll_no': request.user.username,
                'email': request.user.email
            }
        )
        found = Applicant.objects.filter(roll_number=request.user.username)
        logger.error(len(found))
        logger.error(request.user.username)
        if len(found) >= 1:
            filled = True
    return render(request, "portal/apply.html", {"form": form, 'filter': filter, "filled": filled})


@login_required
def waitlist(request):
    user_roll_number = request.user.username
    applicants = Applicant.objects.filter(roll_number=user_roll_number)
    waiting = {}
    feedback = ''
    all_verified = False
    status = ''
    for applicant in applicants:
        waiting['Type - 1'] = applicant.waitlist_Type1
        waiting['Tulsi'] = applicant.waitlist_Tulsi
        waiting['MRSB'] = applicant.waitlist_MRSB
        feedback = applicant.feedback
        all_verified = applicant.all_verified()
        if applicant.acad_details_verified:
            status = "Your application has successfully reached the HCU office."
        else:
            status = "Your application is with the Academic Office."
    return render(request, "portal/waitlist.html", {"waitlist": waiting, "feedback": feedback, "all_verified": all_verified, "status": status})

@login_required
def occupy(request):
    filter = 'Type-1'
    _, eligible_Type1 = get_waitlistType1()
    _, eligible_Tulsi = get_waitlistTulsi()
    _, eligible_MRSB = get_waitlistMRSB()
    applicants = Applicant.objects.filter(roll_number=request.user.username)
    for applicant in applicants:
        if applicant.name in eligible_Type1:
            filter = 'Type-1'
        elif applicant.name in eligible_Tulsi:
            filter = 'Tulsi'
        elif applicant.name in eligible_MRSB:
            filter = 'MRSB'
        else:
            filter = 'Sorry'
    now = datetime.datetime.now()
    is_visible = False
    if now.hour >= 9 and now.hour <= 24:
        print('here')
        is_visible = True
    else:
        is_visible = False
    if request.method == "POST":
        POST = request.POST
        form = OccupyingForm(POST, request.FILES)
        if form.is_valid():
            applicants = Applicant.objects.filter(roll_number=request.user.username)
            logger.error(form.cleaned_data['occupied_Type1'])
            for applicant in applicants:
                applicant.occupied_Type1 = form.cleaned_data['occupied_Type1']
                applicant.save()
                pass
            # form.save()
            return redirect(reverse("portal:thanks"))
    else:
        form = OccupyingForm()
        logger.error("The form is not posting the data")
    return render(request, "portal/occupy.html", {"form": form, "filter": filter, "is_visible": is_visible})

@login_required
def vacate(request):
    applicants = Applicant.objects.filter(roll_number=request.user.username)
    is_visible = False
    logger.error(applicants)
    for applicant in applicants:
        is_visible = applicant.occupied_MRSB or applicant.occupied_Type1 or applicant.occupied_Tulsi
    if request.method == 'POST':
        POST = request.POST
        form = VacatingForm(POST, request.FILES)
        if form.is_valid():
            # for person in Applicant.objects.filter():
            applicants = Applicant.objects.filter(roll_number=request.user.username)
            for applicant in applicants:
                if form.cleaned_data['vacate']:
                    applicant.save(flag=False)
                    
                pass
            # form.save()
            return redirect(reverse("portal:thanks"))
    else:
        form = VacatingForm()
        logger.error("The form is not posting the data")
    return render(request, "portal/vacate.html", {'form': form, 'is_visible': is_visible})

@login_required
def thanks(request):
    """Thank You Page"""
    return render(request, "portal/thanks.html")

@login_required
def logout(request):
    """Log out."""

    logout(request)
    return render(request, "portal/logout.html",)
