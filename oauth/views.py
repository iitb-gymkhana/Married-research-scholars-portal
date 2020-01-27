import base64

import requests
from django.conf import settings
from django.contrib.auth import get_user_model, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, reverse

from core.models import UserProfile

User = get_user_model()


def client_login(req):

    authorize = settings.AUTHORIZATION_URL
    redirect_uri = settings.REDIRECT_URI
    client_id = settings.CLIENT_ID
    scope = settings.SCOPE
    url = "{}?client_id={}&response_type=code&scope={}&redirect_uri={}".format(
        authorize, client_id, scope, redirect_uri
    )
    print(url)

    return redirect(url)


def authenticated(req):
    authCode = req.GET.get("code")

    usrPass = "{}:{}".format(settings.CLIENT_ID, settings.CLIENT_SECRET)
    authenticationToken = base64.b64encode(usrPass.encode("utf-8")).decode("utf-8")
    headers = {
        "Authorization": "Basic {}".format(authenticationToken),
        "Content-type": "application/x-www-form-urlencoded",
    }
    data = (
        "code="
        + authCode
        + "&redirect_uri="
        + settings.REDIRECT_URI
        + "&grant_type=authorization_code"
    )
    response = requests.post(
        settings.SSO_TOKEN_URL, data=data, headers=headers, verify=False
    )

    response_json = response.json()

    # get profile
    profile_response = requests.get(
        settings.SSO_PROFILE_URL,
        headers={"Authorization": "Bearer " + response_json["access_token"]},
        verify=False,
    )

    profile_json = profile_response.json()

    roll_number = profile_json["roll_number"]
    first_name = profile_json["first_name"]
    last_name = profile_json["last_name"]
    room = ""
    hostel = ""
    hostel_name = ""

    if profile_json["insti_address"] is not None:
        room = profile_json["insti_address"]["room"]
        hostel = profile_json["insti_address"]["hostel"]
        hostel_name = profile_json["insti_address"]["hostel_name"]
    # TODO: refresh_token = response_json['refresh_token']

    params = [roll_number, first_name, last_name]
    checkEmpty(params)

    try:
        user = User.objects.get(username=profile_json["roll_number"])

    except ObjectDoesNotExist:
        user = User.objects.create_user(
            username=roll_number,
            first_name=first_name.title(),
            last_name=last_name.title(),
            email="{}@iitb.ac.in".format(roll_number),
        )
        user.save()

    try:
        UserProfile.objects.get(user=user)
        # TODO: check for any updates on SSO server
    except UserProfile.DoesNotExist:
        UserProfile.objects.get_or_create(
            user=user, hostel=hostel, hostel_name=hostel_name, room=room
        )

    login(req, user)
    return HttpResponseRedirect(reverse("portal:home"))


def checkEmpty(params):
    for parameter in params:
        if parameter == "":
            return redirect("https://gymkhana.iitb.ac.in/sso/user/")


def client_logout(req):
    logout(req)
    return render(req, "portal/logout.html")
