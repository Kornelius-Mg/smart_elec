from django.conf.urls import url
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

urlpatterns = [
    # URLS d'authentification

    url(r'^logout/$', LogoutView.as_view(template_name="login.html"), name="logout"),
    url(r'^login/$', LoginView.as_view(template_name='login.html'), name="login"),
    url(r'^register/$', register_form, name="register"),
    path('superviseurs/list/', SuperviseurList.as_view(), name='list-superviseurs'),
    path('superviseur/details/', superviseur_details, name='superviseur'),
    path('superviseur/delete/', delete_admin, name="delete-admin"),
    path('superviseur/update', superviseur_update, name="update-admin"),
]