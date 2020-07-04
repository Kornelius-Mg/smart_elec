from django.shortcuts import render, redirect
from django.core import serializers
from django.http import HttpResponse, Http404
from django.db.models import Q
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, TemplateView, DetailView, FormView, View
from app.models import *
from AdminApp.forms import UtilisateurForm, CreateAppartForm
from . import compteurs_states, transfos_states

# Create your views here.




class HomeView(TemplateView):
    template_name = "admin/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["utilisateurs"] = Utilisateur.objects.all()
        context["Abonnements"] = Abonnement.objects.order_by("-date_heure")
        context["transferts"] = TransfertCredit.objects.order_by("-date_heure")
        context["compteurs"] = Compteur.objects.all()
        context["details"] = DetailsCompteur.objects.all()
        return context


# Vues en rapport avec l'utilisateur

class UserCreateView(CreateView):
    model = Utilisateur
    template_name = "admin/create-user.html"
    success_url = "/admin-snel/users/"
    form_class = UtilisateurForm

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context["action"] = "Enregistrer"
        return context

class UserUpdateView(UpdateView):
    model = Utilisateur
    template_name = "admin/update-user.html"
    success_url = "/admin-snel/users/"
    fields = ("nom", "postnom", "prenom", "psw", "telephone")

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context["action"] = "Modifier"
        return context

class UserDeleteView(DeleteView):
    model = Utilisateur
    template_name = "whats-up.html"
    success_url = "/admin-snel/users/"

class UserListView(ListView):
    model = Utilisateur
    template_name = "admin/users.html"
    context_object_name = "users"

class UserDetailView(DetailView):
    model = Utilisateur
    template_name='admin/user.html'
    context_object_name = "user"

    def get(self, request, *args, **kwargs):
        request.session["user"] = kwargs["pk"]
        return super(UserDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context["apparts"] = self.object.appartement_set.all()
        context["nb_apparts"] = self.object.appartement_set.count()
        nb = 0
        for appart in context["apparts"]:
            nb += appart.compteur_set.count()
        context["nb_compteurs"] = nb
        return context

# Vues pour adresses et appartements

class AdresseCreateView(CreateView):
    model = Adresse
    template_name = "admin/create-appart.html"
    fields = ("pays", "province", "ville", "commune", "quartier", "avenue", "numero")
    success_url = "/admin-snel/apparts/new"

    def get(self, request,  *args, **kwargs):
        return super(AdresseCreateView, self).get(request, *args, **kwargs)

class AppartementCreateView(View):
    def get(self, request, *args, **kwargs):
        adresse = list(Adresse.objects.all())[-1]
        appart = Appartement(utilisateur=Utilisateur.objects.get(id=request.session["user"]), adresse=adresse)
        appart.save()
        return redirect("/admin-snel/user/%s"%request.session["user"])

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request!')

class AdresseDeleteView(DeleteView):
    model = Adresse
    template_name = "whats-up.html"

    def get(self, request, *args, **kwargs):
        AdresseDeleteView.success_url = "/admin-snel/user/%s"%request.session["user"]
        return super(AdresseDeleteView, self).get(request, *args, **kwargs)

class AdresseUpdateView(UpdateView):
    model = Adresse
    template_name = "admin/update-appart.html"
    fields = ("pays", "province", "ville", "commune", "quartier", "avenue", "numero")
    
    def get(self, request, *args, **kwargs):
        AdresseUpdateView.success_url = "/admin-snel/user/" + request.session["user"]
        return super(AdresseUpdateView, self).get(request, *args, **kwargs)


# Vues concernant les compteurs


class CompteurAppartListView(ListView):
    model = Compteur
    template_name = "admin/compteurs.html"
    context_object_name = "compteurs"
    
    def get(self, request, **kwargs):
        cle = kwargs["pk"]
        self.key = cle
        CompteurAppartListView.queryset = Appartement.objects.get(id=cle).compteur_set.all()
        return super(CompteurAppartListView, self).get(request, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(CompteurAppartListView, self).get_context_data(**kwargs)
        context["url"] = "compteurs-appart"
        context["id_appart"] = self.key
        return context

class CompteurListView(ListView):
    model = Compteur
    template_name = "admin/compteurs.html"
    context_object_name = "compteurs"
    queryset = Compteur.objects.all()


class CompteurTransfoListView(ListView):
    model = Compteur
    template_name = "agdmin/compteurs.html"
    context_object_name = "compteurs"

class CompteurCreateView(CreateView):
    model = Compteur
    template_name = "admin/create-compteur.html"
    fields = ("modele", "appartement", "transformateur", "active_class")
    success_url = "/admin-snel/compteurs/"

    def get_context_data(self, **kwargs):
        context = super(CompteurCreateView, self).get_context_data(**kwargs)
        context["apparts"] = Appartement.objects.all()
        context["transfos"] = Transformateur.objects.all()
        return context

class CompteurAppartCreateView(CreateView):
    model = Compteur
    template_name = "admin/create-compteur.html"
    fields = ("modele", "appartement", "transformateur", "active_class")

    def get(self, request, **kwargs):
        self.key = kwargs["pk"]
        CompteurAppartCreateView.success_url = "/admin-snel/compteurs-appart/"+self.key
        return super(CompteurAppartCreateView, self).get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CompteurAppartCreateView, self).get_context_data(**kwargs)
        context["apparts"] = Appartement.objects.all()
        context["id_appart"] = list(context["apparts"]).index(Appartement.objects.get(id=self.key)) + 1
        context["transfos"] = Transformateur.objects.all()
        return context


class DetailsCompteurView(DetailView):
    model = Compteur
    template_name = "admin/compteur.html"
    context_object_name = "compteur"

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            JSONSerializer = serializers.get_serializer("json")
            json_serializer = JSONSerializer()
            json_serializer.serialize(DetailsCompteur.objects.order_by("-instant").filter(compteur=Compteur.objects.get(id=kwargs["pk"])))
            datas = json_serializer.getvalue()
            return HttpResponse(datas)
        else:
            return super(DetailsCompteurView, self).get(request, *args, **kwargs) 

    def get_context_data(self, **kwargs):
        context = super(DetailsCompteurView, self).get_context_data(**kwargs)
        context['details'] = Compteur.objects.get(id=self.object.pk).detailscompteur_set.order_by("-instant")
        return context



class CompteurDeleteView(DeleteView):
    model = Compteur
    template_name = "whats-up.html"
    success_url = "/admin-snel/compteurs"


class CompteurUpdateView(UpdateView):
    model = Compteur
    template_name = "admin/update-compteur.html"
    success_url = "/admin-snel/compteurs"
    fields = ("modele", "appartement", "transformateur", "active_class")

    def get_context_data(self, **kwargs):
        context = super(CompteurUpdateView, self).get_context_data(**kwargs)
        context["apparts"] = Appartement.objects.all()
        context["id_appart"] = list(context["apparts"]).index(self.object.appartement) + 1
        context["transfos"] = Transformateur.objects.all()
        context["id_transfo"] = list(context["transfos"]).index(self.object.transformateur) + 1
        return context

# Vues concernant les transformateurs

class TransformateurListView(ListView):
    model = Transformateur
    template_name = "admin/transfos.html"
    context_object_name = "transfos"


class TransformateurDetailView(DetailView):
    model = Transformateur
    template_name = "admin/transfo.html"
    context_object_name = "transfo"

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            JSONSerializer = serializers.get_serializer("json")
            json_serializer = JSONSerializer()
            json_serializer.serialize(DetailsTransfo.objects.order_by("-instant").filter(transformateur=Transformateur.objects.get(id=kwargs["pk"])))
            datas = json_serializer.getvalue()
            return HttpResponse(datas)
        else:
            return super(TransformateurDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TransformateurDetailView, self).get_context_data(**kwargs)
        context['compteurs'] = Transformateur.objects.get(id=self.object.pk).compteur_set.all()
        context['details'] = Transformateur.objects.get(id=self.object.pk).detailstransfo_set.order_by("-instant")
        return context


class TransformateurCreateView(CreateView):
    model = Transformateur
    template_name = "admin/create-transfo.html"
    success_url = "/admin-snel/transfos/"
    fields = ("designation", "p_max", "q_max")


class TransformateurUpdateView(UpdateView):
    model = Transformateur
    template_name = "admin/update-transfo.html"
    fields = ("designation", "p_max", "q_max")
    success_url = "/admin-snel/transfos/"


class TransformateurDeleteView(DeleteView):
    model = Transformateur
    template_name = "whats-up.html"
    success_url = "/admin-snel/transfos/"

# AJAX REQUESTS

def transformateur_infos(request, *args, **kwargs):
    if request.is_ajax():
        JSONSerializer = serializers.get_serializer("json")
        json_serializer = JSONSerializer()
        json_serializer.serialize(Transformateur.objects.filter(id=kwargs["pk"]))
        datas = json_serializer.getvalue()
        return HttpResponse(datas)


def compteur_infos(request, *args, **kwargs):
    if request.is_ajax():
        JSONSerializer = serializers.get_serializer("json")
        json_serializer = JSONSerializer()
        json_serializer.serialize( Compteur.objects.filter(id=kwargs["pk"]))
        datas = json_serializer.getvalue()
        return HttpResponse(datas)

def start_transfo(request, *args, **kwargs):
    if request.method == "GET":
        responses = transfos_states.get_infos()
        if responses:
            id_t = kwargs["pk"]
            transfo = Transformateur.objects.get(id=id_t)
            transfo.global_state = "ON"
            transfo.save()
            return HttpResponse("ok")
        else:
            return Http404

def stop_transfo(request, *args, **kwargs):
    if request.method == "GET":
        responses = transfos_states.get_infos()
        if responses:
            d_t = kwargs["pk"]
            transfo = Transformateur.objects.get(id=id_t)
            transfo.global_state = "OFF"
            transfo.save()
            return HttpResponse("ok")
        else:
            return Http404

def start_compteur(request, *args, **kwargs):
    if request.method == "GET":
        responses = compteurs_states.get_infos()
        if responses:
            id_c = kwargs["pk"]
            compteur = Compteur.objects.get(id=id_c)
            compteur.global_state = "ON"
            compteur.save()
            return HttpResponse("ok")
        else:
            return Http404

def stop_compteur(request, *args, **kwargs):
    if request.method == "GET":
        responses = compteurs_states.get_infos()
        if responses:
            d_c = kwargs["pk"]
            compteur = Compteur.objects.get(id=id_c)
            compteur.global_state = "OFF"
            compteur.save()
            return HttpResponse("ok")
        else:
            return Http404