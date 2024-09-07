from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from tablib import Dataset

# Create your views here.
from .models import UserAsistente, UserCoordinador
from .forms import UsuariosForm
from .mixins import GroupRequiredMixin
from .resources import AsistenteResource, CoordinadorResource

class PerfilHome(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.groups.filter(name='coordinador').exists():
                return redirect('coordinador_home')
            else:
                return render(request, 'usuarios/usuario_home.html')
        else:
            return redirect('home')


class InscriptosList(GroupRequiredMixin, ListView):
    model = UserAsistente
    template_name = 'usuarios/coordinador_home.html'
    group_name = 'coordinador'
    
    def get_queryset(self):
        usuario_actual = UserCoordinador.objects.get(user=self.request.user)
        dependencias = usuario_actual.dependencia.all()
        return UserAsistente.objects.filter(dependencia__in=dependencias).distinct()


class UsuariosCreateView(GroupRequiredMixin, CreateView):
    group_name = 'coordinador'
    model = UserAsistente
    form_class = UsuariosForm
    template_name = 'usuarios/create_uno.html'
    success_url = 'coordinador_home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agrega un título para la página
        context['title'] = 'Registro de Usuario'
        return context
    

def import_users(request):
    if request.method == 'POST':
        user_resource = AsistenteResource()
        dataset = Dataset()
        new_users = request.FILES['myfile']

        try:
            imported_data = dataset.load(new_users.read(), format='xlsx')
            result = user_resource.import_data(
                dataset, dry_run=True)  # Simulación de la importación
            print(imported_data)

            if result.has_errors():
                # Recopilar los errores para mostrarlos
                error_list = []
                for row_errors in result.row_errors():
                    row_num = row_errors[0]
                    errors = row_errors[1]
                    error_list.append(f"Fila {row_num}: {', '.join([str(e.error) for e in errors])}")

                messages.error(
                    request, f"Errores durante la importación:\n{error_list}")
            else:
                # Realiza la importación real
                user_resource.import_data(dataset, dry_run=False)
                messages.success(request, "Usuarios importados con éxito.")
        except Exception as e:
            messages.error(request, f"Error durante la importación: {str(e)}")

        return redirect('coordinador_inscribir_muchos')

    return render(request, 'usuarios/import.html')


class EditarAsistente(GroupRequiredMixin, UpdateView):
    model = UserAsistente
    form_class = UsuariosForm
    group_name = 'coordinador'
    template_name = 'editar_producto.html'
    success_url = 'coordinador_home'
    
    
class EliminarAsistente(GroupRequiredMixin, DeleteView):
    model = UserAsistente
    template_name = 'confirmar_eliminacion.html'
    success_url = 'coordinador_home'
