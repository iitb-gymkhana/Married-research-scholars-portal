from django.urls import path

from .views import apply, portal, waitlist, vacate, thanks
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path("", portal, name="home"),
    path("apply/", apply, name="apply"),
    path("waitlist/", waitlist, name="waitlist"),
    path("thanks/", thanks, name="thanks"),
    path("vacate/", vacate, name='vacate'),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog')
]
