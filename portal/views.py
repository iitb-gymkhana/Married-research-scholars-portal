from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import ApplicantForm, VacatingForm
from django.core.mail import send_mail
from django.conf import settings
from .models import Applicant


@login_required
def portal(request):
    return render(request, "portal/home.html")


@login_required
def apply(request):
    filter = ['spouse_name', 'spouse_roll_number', 'spouse_designation']
    filled = False
    try:
        initial_instance = Applicant.objects.get(roll_number=request.user.username)
    except:
        initial_instance = None
    if request.method == "POST":
        POST = request.POST
        form = ApplicantForm(POST, files=request.FILES, instance=initial_instance)
        # TODO: can't sent in POST requests when fields are disabled,.
        if form.is_valid():
            # model = form.instance
            # all_fields = model._meta.fields
            # _, __ = Applicant.objects.update_or_create(*all_fields)
            model = form.instance
            model.save(flag=True)
            return redirect(reverse("portal:thanks"))
    else:
        form = ApplicantForm(
            # initial={
            #     'name': request.user.first_name + ' ' + request.user.last_name,
            #     'roll_number': request.user.username,
            #     'email': request.user.email
            # },
            instance=initial_instance
        )
        # found = Applicant.objects.filter(roll_number=request.user.username)
        # if len(found) >= 1:
        #     filled = True
    return render(request, "portal/apply.html", {"form": form, 'filter': filter, "filled": filled})


@login_required
def waitlist(request):
    user_roll_number = request.user.username
    applicants = Applicant.objects.filter(roll_number=user_roll_number)
    waiting = {}
    feedback = ''
    acad_feedback = ''
    all_verified = False
    status = 'You have not filled the application'
    for applicant in applicants:
        waiting['Type - 1'] = applicant.waitlist_Type1
        waiting['Tulsi'] = applicant.waitlist_Tulsi
        waiting['Manas'] = applicant.waitlist_MRSB
        feedback = applicant.feedback
        acad_feedback = applicant.acadsection_feedback
        all_verified = applicant.all_verified()
        if not applicant.acad_details_verified:
            status = "Your application is with the Academic Office. " + acad_feedback
        elif applicant.acad_details_verified and not all_verified:
            status = "Your application is with the HCU office."
        else:
            status = "Your application is with the HCU office."
        print(status)
    return render(request, "portal/waitlist.html", {"waitlist": waiting, "feedback": feedback, "all_verified": all_verified, "status": status})

# @login_required
# def occupy(request):
#     filter = 'Sorry'
#     _, eligible_Type1 = get_waitlistType1()
#     _, eligible_Tulsi = get_waitlistTulsi()
#     _, eligible_MRSB = get_waitlistMRSB()
#     applicants = Applicant.objects.filter(roll_number=request.user.username)
#     for applicant in applicants:
#         if applicant.name in eligible_Type1:
#             filter = 'Type-1'
#         elif applicant.name in eligible_Tulsi:
#             filter = 'Tulsi'
#         elif applicant.name in eligible_MRSB:
#             filter = 'MRSB'
#         else:
#             filter = 'Sorry'
#     now = datetime.datetime.now()
#     is_visible = False
#     if now.hour >= 9 and now.hour <= 24:
#         is_visible = True
#     else:
#         is_visible = False
#     if request.method == "POST":
#         POST = request.POST
#         form = OccupyingForm(POST, request.FILES)
#         if form.is_valid():
#             applicants = Applicant.objects.filter(roll_number=request.user.username)
#             for applicant in applicants:
#                 applicant.occupied_Type1 = form.cleaned_data['occupied_Type1']
#                 applicant.defer_Type1 = form.cleaned_data['defer_Type1']
#                 applicant.occupied_Tulsi = form.cleaned_data['occupied_Tulsi']
#                 applicant.defer_Tulsi = form.cleaned_data['defer_Tulsi']
#                 applicant.occupied_MRSB = form.cleaned_data['occupied_MRSB']
#                 applicant.defer_MRSB = form.cleaned_data['defer_MRSB']
#                 applicant.save()
#                 pass
#             # form.save()
#             return redirect(reverse("portal:thanks"))
#     else:
#         form = OccupyingForm()
#     return render(request, "portal/occupy.html", {"form": form, "filter": filter, "is_visible": is_visible})

@login_required
def vacate(request):
    applicants = Applicant.objects.filter(roll_number=request.user.username)
    is_visible = False
    for applicant in applicants:
        # is_visible = applicant.occupied_MRSB or applicant.occupied_Type1 or applicant.occupied_Tulsi
        is_visible = applicant.occupied_any()
    if request.method == 'POST':
        POST = request.POST
        form = VacatingForm(POST, request.FILES)
        if form.is_valid():
            # for person in Applicant.objects.filter():
            applicants = Applicant.objects.filter(roll_number=request.user.username)
            for applicant in applicants:
                if form.cleaned_data['vacate']:
                    building = ''
                    if applicant.occupied_Type1:
                        applicant.occupied_Type1 = False
                        applicant.occupied_Tulsi = True
                        applicant.occupied_MRSB = True
                        building = 'Type-1'
                    elif applicant.occupied_Tulsi:
                        applicant.occupied_Type1 = True
                        applicant.occupied_Tulsi = False
                        applicant.occupied_MRSB = True
                        building = 'Tulsi'
                    elif applicant.occupied_MRSB:
                        applicant.occupied_Type1 = True
                        applicant.occupied_Tulsi = True
                        applicant.occupied_MRSB = False
                        building = 'Manas'
                    else:
                        pass
                    applicant.save(flag=False)
                emailid = applicant.email
                message = f"You have successfully vacated {building}. Deposit the keys at HCU office."
                subject = "Married Research Scholar Portal"
                send_mail(
                    subject=subject,
                    message=message,
                    recipient_list=[emailid, ],
                    from_email=settings.DEFAULT_FROM_MAIL
                )
                pass
            # form.save()
            return redirect(reverse("portal:thanks"))
    else:
        form = VacatingForm()
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
