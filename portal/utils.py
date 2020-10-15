from .models import Applicant
from django.core.mail import send_mail
from django.conf import settings
import datetime

TYPE1 = 4  # Total Capacity
TULSI = 4  # Total Capacity
MRSB = 4  # Total Capicity

def get_waitlistType1():
    waitlist = list(Applicant.objects.order_by('waitlist_Type1'))
    TYPE1_VACANT = TYPE1 - len(Applicant.objects.filter(occupied_Type1=True))
    recepient_emails = []
    recepients = []
    for i in range(TYPE1_VACANT):
        recepient_emails.append(waitlist[i].email)
        recepients.append(waitlist[i].name)
    return recepient_emails, recepients
    


def get_waitlistTulsi():
    waitlist = list(Applicant.objects.order_by('waitlist_Tulsi'))
    TULSI_VACANT = TULSI - len(Applicant.objects.filter(occupied_Tulsi=True))
    recepient_emails = []
    recepients = []
    for i in range(TULSI_VACANT):
        recepient_emails.append(waitlist[i].email)
        recepients.append(waitlist[i].name)
    return recepient_emails, recepients


def get_waitlistMRSB():
    waitlist = list(Applicant.objects.order_by('waitlist_Type1'))
    MRSB_VACANT = MRSB - len(Applicant.objects.filter(occupied_MRSB=True))
    recepient_emails = []
    recepients = []
    for i in range(MRSB_VACANT):
        recepient_emails.append(waitlist[i].email)
        recepients.append(waitlist[i].name)
    return recepient_emails, recepients

def send_notifs_to_students():
    recepients_Type1, _ = get_waitlistType1()
    recepients_Tulsi, _ = get_waitlistTulsi()
    recepients_MRSB, _ = get_waitlistMRSB()
    subject = "Married Research Scholar Accomodation"
    message = "You are now eligible to occupy {}. If you wish to occupy, kindly do it in the MRSP Portal by tonight!"
    now = datetime.datetime.now()
    now_ = 0
    if now.hour == 0:
        send_mail(subject, message.format('Type-1'), from_email=settings.EMAIL_HOST_USER, recipient_list=recepients_Type1)
        send_mail(subject, message.format('Tulsi'), from_email=settings.EMAIL_HOST_USER, recipient_list=recepients_Tulsi)
        send_mail(subject, message.format('MRSB'), from_email=settings.EMAIL_HOST_USER, recipient_list=recepients_MRSB)
        now_ = now
    return now_
