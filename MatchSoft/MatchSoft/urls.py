# MatchSoft/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),   # La raíz apunta a tu app 'core'
]
