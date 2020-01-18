from django.urls import path

from .views import apply, portal, waitlist

urlpatterns = [
    path("", portal, name="home"),
    path("apply/", apply, name="apply"),
    # waitlist and thanks have the same page.
    path("waitlist/", waitlist, name="waitlist"),
    path("thanks/", waitlist, name="thanks"),
]
