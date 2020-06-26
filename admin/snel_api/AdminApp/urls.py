from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from AdminApp.views import *
from django.conf.urls import url


urlpatterns = [
     path('', HomeView.as_view(), name="home"),

     # Urls pour utilisateurs
     path('users/new', UserCreateView.as_view(), name="new-user"),
     path('users/', UserListView.as_view(), name="users"),
     url(r'^users/delete/(?P<pk>[0-9]+)/$', UserDeleteView.as_view(), name="delete-user"),
     url(r'^users/update/(?P<pk>[0-9]+)/$', UserUpdateView.as_view(), name="update-user"),
     url(r'^user/(?P<pk>[0-9]+)/$', UserDetailView.as_view(), name="user"),

     # Urls pour appartements et adresses
     url(r'^adresses/new/(?P<pk>[0-9]+)/$', AdresseCreateView.as_view(), name="new-adresse"),
     url(r'^apparts/update/(?P<pk>[0-9]+)/$', AdresseUpdateView.as_view(), name="update-appart"),
     url(r'^apparts/delete/(?P<pk>[0-9]+)/$', AdresseDeleteView.as_view(), name="delete-appart"),
     url(r'^apparts/new/$', AppartementCreateView.as_view(), name="new-appart"),

     # Urls pour compteurs
     url(r'^compteurs/new/$', CompteurCreateView.as_view(), name="new-compteur"),
     url(r'^compteurs-appart/(?P<pk>[0-9]+)/$', CompteurAppartListView.as_view(), name="compteurs-appart"),
     url(r'^compteurs-appart/(?P<pk>[0-9]+)/new/$', CompteurAppartCreateView.as_view(), name="new-compteur-appart"),
     url(r'^compteurs/$', CompteurListView.as_view(), name="compteurs"),
     url(r'^compteurs-transfo/(?P<pk>[0-9]+)/$', CompteurTransfoListView.as_view(), name="compteurs-transfo"),
     url(r'compteurs/delete/(?P<pk>[0-9]+)/$', CompteurDeleteView.as_view(), name="delete-compteur"),
     url(r'^compteurs/update/(?P<pk>[0-9]+)/$', CompteurUpdateView.as_view(), name="update-compteur"),
     url(r'^compteur/(?P<pk>[0-9]+)/$', DetailsCompteurView.as_view(), name="compteur"),
     url(r'^compteur-infos/(?P<pk>[0-9]+)/$', compteur_infos, name="compteur-infos"),

     # urls pour transfos
     url(r'^transfos/$', TransformateurListView.as_view(), name="transfos"),
     url(r'^transfos/new/$', TransformateurCreateView.as_view(), name="new-transfo"),
     url(r'^transfos/update/(?P<pk>[0-9]+)/$', TransformateurUpdateView.as_view(), name="update-transfo"),
     url(r'^transfos/delete/(?P<pk>[0-9]+)/$', TransformateurDeleteView.as_view(), name="delete-transfo"),
     url(r'transfo/(?P<pk>[0-9]+)/$', TransformateurDetailView.as_view(), name="transfo"),
     url(r'^transfo-infos/(?P<pk>[0-9]+)/$', transformateur_infos, name="transfo-infos"),
]

# urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)