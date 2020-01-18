from django.urls import path
from django.views.generic import TemplateView

from .views import apply, portal

urlpatterns = [
    path("", portal, name="home"),
    path("apply/", apply, name="apply"),
    path("thanks/", TemplateView.as_view(template_name="thanks.html"), name="thanks"),
]
