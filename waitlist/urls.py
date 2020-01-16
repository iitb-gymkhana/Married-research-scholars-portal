from django.urls import path
from django.views.generic import RedirectView, TemplateView

from .views import application

urlpatterns = [
    # redirect this to apply/
    path("", RedirectView.as_view(pattern_name="waitlist:apply", permanent=False)),
    path("apply/", application, name="apply"),
    path("thanks/", TemplateView.as_view(template_name="thanks.html"), name="thanks"),
]
