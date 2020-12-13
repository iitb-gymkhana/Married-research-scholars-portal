"""married-research-scholar-portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from portal.admin import hcu_admin_site, acad_admin_site

import oauth.urls
import portal.urls

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("oauth/", include((oauth.urls, "oauth"), namespace="oauth")),
    path("portal/", include((portal.urls, "portal"), namespace="portal")),
    path("admin/", admin.site.urls),
    path("hcu/", hcu_admin_site.urls),
    path("acad/", acad_admin_site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
