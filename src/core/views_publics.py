from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView

# Create your views here.


class PerfilHome(TemplateView):
    template_name = "usuarios\perfil_home.html"
