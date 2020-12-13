from django.urls import path

from .views import apply, portal, waitlist, occupy, vacate, thanks

urlpatterns = [
    path("", portal, name="home"),
    path("apply/", apply, name="apply"),
    # waitlist and thanks have the same page.
    path("waitlist/", waitlist, name="waitlist"),
    path("thanks/", thanks, name="thanks"),
    path("occupy/", occupy, name='occupy'),
    path("vacate/", vacate, name='vacate')
]
