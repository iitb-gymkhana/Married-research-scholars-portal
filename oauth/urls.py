from django.urls import path

from .views import authenticated, client_login, client_logout

urlpatterns = [
    path("login/", client_login, name="login"),
    path("callback/", authenticated, name="callback"),
    path("logout/", client_logout, name="logout"),
]
