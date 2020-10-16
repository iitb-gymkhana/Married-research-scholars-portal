from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
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
    if request.method == "POST":
        POST = request.POST
        # POST = request.POST.copy()
        # POST['roll_number'] = request.user.username
        # POST['name'] = request.user.first_name + request.user.last_name
        # POST['email'] = request.user.email
        # form = QueuerForm(POST, request.FILES)
        form = ApplicantForm(POST, request.FILES)
        # TODO: can't sent in POST requests when fields are disabled,.

        if form.is_valid():
            form.save()
            # applicant = Applicant.objects.filter(roll_number=form.cleaned_data['roll_number'])
            # print(applicant)
            # applicant.spouse_name = form2.cleaned_data['spouse_name']
            # applicant.spouse_roll_number = form2.cleaned_data['spouse_roll_number']
            # applicant.spouse_designation = form2.cleaned_data['spouse_designation']
            # applicant.save()
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
    return render(request, "portal/apply.html", {"form": form, 'filter': filter})


@login_required
def waitlist(request):
    user_roll_number = request.user.username
    queues = Queuer.objects.filter(roll_number=user_roll_number)
    applicants = Applicant.objects.filter(roll_number=user_roll_number)
    waiting = {}
    feedback = ''
    all_verified = False
    # print(get_waitlistType1())
    # print(get_waitlistTulsi())
    # print(get_waitlistMRSB())
    # send_notifs()
    # for queue in queues:
    #     waiting["Type - 1"] = queue.waitlist_Type1
    #     waiting['Tulsi'] = queue.waitlist_Tulsi
    #     waiting['MRSB'] = queue.waitlist_MRSB
    for applicant in applicants:
        waiting['Type - 1'] = applicant.waitlist_Type1
        waiting['Tulsi'] = applicant.waitlist_Tulsi
        waiting['MRSB'] = applicant.waitlist_MRSB
        feedback = applicant.feedback
        all_verified = applicant.all_verified()
    return render(request, "portal/waitlist.html", {"waitlist": waiting, "feedback": feedback, "all_verified": all_verified})

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
    if now.hour >= 9 and now.hour <= 17:
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
    return render(request, "portal/occupy.html", {"form": form, "filter": filter})

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
                # applicant.save(flag=True)
                    applicant.delete()
                pass
            # form.save()
            return redirect(reverse("portal:thanks"))
    else:
        form = VacatingForm()
        logger.error("The form is not posting the data")
    return render(request, "portal/vacate.html", {'form': form, 'is_visible': is_visible})

@login_required
def logout(request):
    """Log out."""

    logout(request)
    return render(request, "portal/logout.html",)
