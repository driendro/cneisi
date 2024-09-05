from django.shortcuts import render
from django.views.generic.edit import CreateView

# Create your views here.
from .models import Usuarios
from .forms import UsuariosForm


class UsuariosCreateView(CreateView):
    model = Usuarios
    form_class = UsuariosForm
    template_name = 'usuarios/usuarios_form.html'
    success_url = '/'  # Reemplaza '/' con la URL a la que redirigir después de un envío exitoso

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agrega un título para la página
        context['title'] = 'Registro de Usuario'
        return context
