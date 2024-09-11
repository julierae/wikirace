"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.shortcuts import redirect
from django.urls import include, path

from django.contrib import admin
from django.conf import settings

urlpatterns = [
    path("", lambda request: redirect("wikirace/")),
    path("favicon.ico", lambda request: redirect("/static/images/favicon.ico")),
    path("wikirace/", include("wikirace.urls")),
    path("admin/", admin.site.urls),
]

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
