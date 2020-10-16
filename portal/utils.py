from .models import Applicant
from django.core.mail import send_mail
from django.conf import settings
import datetime
from django.utils import timezone

TYPE1 = 4  # Total Capacity
TULSI = 4  # Total Capacity
MRSB = 4  # Total Capicity

def get_waitlistType1():
    waitlist = list(Applicant.objects.filter(waitlist_Type1__gt=0, defer_Type1=False).order_by('waitlist_Type1'))
    TYPE1_VACANT = TYPE1 - len(Applicant.objects.filter(occupied_Type1=True))
    recepient_emails = []
    recepients = []
    for i in range(TYPE1_VACANT):
        try:
            recepient_emails.append(waitlist[i].email)
            recepients.append(waitlist[i].name)
        except:
            pass
    return recepient_emails, recepients
    


def get_waitlistTulsi():
    waitlist = list(Applicant.objects.filter(waitlist_Tulsi__gt=0, defer_Tulsi=False).order_by('waitlist_Tulsi'))
    TULSI_VACANT = TULSI - len(Applicant.objects.filter(occupied_Tulsi=True))
    recepient_emails = []
    recepients = []
    for i in range(TULSI_VACANT):
        try:
            recepient_emails.append(waitlist[i].email)
            recepients.append(waitlist[i].name)
        except:
            pass
    return recepient_emails, recepients


def get_waitlistMRSB():
    waitlist = list(Applicant.objects.filter(waitlist_MRSB__gt=0, defer_MRSB=False).order_by('waitlist_Type1'))
    MRSB_VACANT = MRSB - len(Applicant.objects.filter(occupied_MRSB=True))
    recepient_emails = []
    recepients = []
    for i in range(MRSB_VACANT):
        try:
            recepient_emails.append(waitlist[i].email)
            recepients.append(waitlist[i].name)
        except:
            pass
    return recepient_emails, recepients

def send_notifs_to_students():
    recepients_Type1, _ = get_waitlistType1()
    recepients_Tulsi, _ = get_waitlistTulsi()
    recepients_MRSB, _ = get_waitlistMRSB()
    subject = "Married Research Scholar Accomodation"
    message = "You are now eligible to occupy {}. If you wish to occupy, kindly do it in the MRSP Portal between 9AM to 5PM tomorrow"
    now = datetime.datetime.now()
    now_ = 0
    if now.hour == 23 and now.minute == 50:
        send_mail(subject, message.format('Type-1'), from_email=settings.EMAIL_HOST_USER, recipient_list=recepients_Type1)
        send_mail(subject, message.format('Tulsi'), from_email=settings.EMAIL_HOST_USER, recipient_list=recepients_Tulsi)
        send_mail(subject, message.format('MRSB'), from_email=settings.EMAIL_HOST_USER, recipient_list=recepients_MRSB)
        now_ = now
    print("Notification Sent to Student at {}".format(now_))

def send_notifs_to_ARHCU():
    recepient = ['mmkipsit@gmail.com']
    subject = "Married Research Scholar Portal Updates"
    num_New_Applications = len(Applicant.objects.filter(
        occupied_Type1 = False,
        occupied_Tulsi = False,
        occupied_MRSB = False,
        marriage_certificate_verified = False,
        joint_photograph_with_spouse_verified = False,
        coursework_grade_sheet_verified = False,
        recommendation_of_guide_for_accomodation_verified = False
    ))
    message = "You have {} new applications waiting to get verified".format(num_New_Applications)
    now = datetime.datetime.now()
    if now.hour == 6:
        send_mail(subject, message, from_email=settings.EMAIL_HOST_USER, recipient_list=recepient)
        print("Notification sent to ARHCU at {}".format(now))

    
