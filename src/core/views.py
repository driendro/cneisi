from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseNotAllowed
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.views import View
from django.views.generic import TemplateView, DeleteView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from tablib import Dataset
import threading
from datetime import date

# Create your views here.
from .models import UserAsistente, UserCoordinador, Actividad, Dependencia
from .forms import UsuariosForm, AsistenteUpdateForm,generar_cadena_alternante
from .mixins import GroupRequiredMixin
from .resources import AsistenteResource, CoordinadorResource

def create_email(user_mail, subject, template_name, context):
    template = get_template(template_name)
    content = template.render(context=context)

    message = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[
            user_mail
        ],
        cc=[]
    )
    
    message.attach_alternative(content, 'text/html')
    return message

###############################Publicas########################################################################################################################
###############################Publicas########################################################################################################################
###############################Publicas########################################################################################################################
###############################Publicas########################################################################################################################
###############################Publicas########################################################################################################################

class PerfilHome(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('staff_home')
            elif request.user.groups.filter(name='coordinador').exists():
                return redirect('coordinador_home')
            elif request.user.groups.filter(name='asistente').exists():
                return redirect('asistente_home')
            else:
                return redirect('home')
        else:
            return redirect('home')

class LandingPage(TemplateView):
    model = Actividad
    template_name = 'landing/home.html'
    context_object_name = 'actividades'
    
    def get_context_data(self, **kwargs):
        # En el Contexto se van a renderizar segun la fecha de la actividad, para poder mostrarlas mas facil en el home
        context = super().get_context_data(**kwargs)
        context['actividades'] = Actividad.objects.all()
        context['actividad_25'] = Actividad.objects.filter(fecha=date(2024, 10, 25)).all()
        context['actividad_26']=Actividad.objects.filter(fecha=date(2024,10,26)).all()
        context['actividad_27']=Actividad.objects.filter(fecha=date(2024,10,27)).all()
        # Agrega un título para la página
        context['title'] = 'Registro de Usuario'
        return context



###############################Coordinador########################################################################################################################
###############################Coordinador########################################################################################################################
###############################Coordinador########################################################################################################################
###############################Coordinador########################################################################################################################
###############################Coordinador########################################################################################################################

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
    success_url = reverse_lazy('coordinador_inscribir_uno')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agrega un título para la página
        context['title'] = 'Registro de Usuario'
        return context

    def get_form_kwargs(self):
        # Obtener los kwargs originales
        kwargs = super(UsuariosCreateView, self).get_form_kwargs()
        # Añadir el usuario al diccionario de kwargs
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        # Esto es la instancia completa, no el ID
        dependencia = form.cleaned_data.get('dependencia')
        asistentes = UserAsistente.objects.filter(dependencia=dependencia)

        if dependencia.cupo == 0 or dependencia.cupo > asistentes.count():  # cupo es un atributo de 'dependencia'
            return super().form_valid(form)
        else:
            # Agrega un mensaje de error al formulario
            form.add_error(None, 'No hay suficientes cupos disponibles. El cupo de su dependencia es: {}'.format(
                dependencia.cupo))
            # Llama a form_invalid si falla la validación
            return self.form_invalid(form)
        

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
    form_class = AsistenteUpdateForm
    group_name = 'coordinador'
    template_name = 'usuarios/update_uno.html'
    success_url = reverse_lazy('coordinador_home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agrega un título para la página
        context['title'] = 'Actualizar datos del Asistente'
        return context


class EliminarAsistente(GroupRequiredMixin, DeleteView):
    model = UserAsistente
    group_name = 'coordinador'
    template_name = 'confirmar_eliminacion.html'
    success_url = reverse_lazy('coordinador_home')


class DetalleAsistente(GroupRequiredMixin, DetailView):
    model = UserAsistente
    group_name = 'coordinador'
    template_name = 'usuarios/view_uno.html'  # Template que usaremos
    context_object_name = 'user_asistente'  # Nombre con el que accederás al objeto en la plantilla
    


###############################Asistente########################################################################################################################
###############################Asistente########################################################################################################################
###############################Asistente########################################################################################################################
###############################Asistente########################################################################################################################
###############################Asistente########################################################################################################################

class AsistenteHome(GroupRequiredMixin, TemplateView):
    model = UserAsistente
    group_name = 'asistente'
    template_name = 'asistente/home.html'
    context_object_name = 'user_asistente'

    def get_context_data(self, **kwargs):
        # Obtener el contexto base
        context = super().get_context_data(**kwargs)
        # Obtener el usuario autenticado
        user = self.request.user
        # Obtener el objeto UserAsistente correspondiente al usuario autenticado
        asistente = UserAsistente.objects.get(user=user)
        # Obtener todas las actividades
        actividades = Actividad.objects.all()
        # Obtener las actividades en las que el asistente está inscrito desde el modelo Actividad
        actividades_inscritas = Actividad.objects.filter(asistentes=asistente)
        # Filtrar actividades no inscritas
        actividades_no_inscritas = actividades.exclude(id__in=actividades_inscritas.values_list('id', flat=True))
        # Agregar al contexto todas las actividades y las inscritas
        context['actividades_no_inscritas'] = actividades_no_inscritas
        context['actividades_inscritas'] = actividades_inscritas
        return context


@login_required
def inscribirse(request, actividad_id):
    if request.method == 'POST':
        actividad = get_object_or_404(Actividad, id=actividad_id)
        cupo = actividad.aula.cupo
        user_asistente = request.user.userasistente
        if user_asistente not in actividad.asistentes.all():
            if actividad.asistentes.count()>cupo-1 and not cupo==0:
                actividad.habilitada = False
                actividad.save()
            actividad.asistentes.add(user_asistente)
        return redirect('asistente_home')  # Redirige a la vista deseada
    return HttpResponseNotAllowed(['POST'])


@login_required
def desinscribirse(request, actividad_id):
    if request.method == 'POST':
        actividad = get_object_or_404(Actividad, id=actividad_id)
        cupo = actividad.aula.cupo
        user_asistente = request.user.userasistente
        if user_asistente in actividad.asistentes.all():
            if actividad.asistentes.count() <= cupo+1:
                actividad.habilitada = True
                actividad.save()
            actividad.asistentes.remove(user_asistente)
        return redirect('asistente_home')  # Redirige a la vista deseada
    return HttpResponseNotAllowed(['POST'])


############################### Django_Staff ########################################################################################################################
############################### Django_Staff ########################################################################################################################
############################### Django_Staff ########################################################################################################################
############################### Django_Staff ########################################################################################################################
############################### Django_Staff ########################################################################################################################

class StaffHome(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Actividad
    template_name = 'admin/home.html'
    context_object_name = 'actividades'
    
    def test_func(self):
        return self.request.user.is_staff
    
    
def abir_inscripciones(request):
    if request.user.is_authenticated and request.user.is_staff and request.method == 'POST':
        thread = threading.Thread(
            target=lambda: Actividad.objects.all().update(inscripcion=True))
        thread.start()
        return redirect('staff_home')  # Redirige a la vista deseada
    else:
        return redirect('home')  # Redirige a la vista deseada


def cerrar_inscripciones(request):
    if request.user.is_authenticated and request.user.is_staff and request.method == 'POST':
        Actividad.objects.all().update(inscripcion=False)
        return redirect('staff_home')  # Redirige a la vista deseada
    else:
        return redirect('home')  # Redirige a la vista deseada


def envio_correos_inscripcion(request):
    if request.user.is_authenticated and request.user.is_staff:
        # Llamar al método save del formulario para obtener la instancia y la contraseña
        asistentes = UserAsistente.objects.all()
        for asistente in asistentes:
            nombre = asistente.user.first_name
            correo = asistente.user.email
            dependencia = asistente.dependencia.nombre_largo
            username = asistente.user.username
            password = asistente.documento
    
            # Crear y enviar el correo
            email = create_email(
                user_mail=correo,
                subject='Confirmación de Inscripción al CNEISI',
                template_name='correos/inscripcion.html',
                context={
                    'usuario': username,  # Enviar el nombre de usuario
                    'nombre': nombre,  # Enviar el nombre del usuario
                    'dependencia': dependencia,
                    'password': password,
                    'url': 'https://cneisi.frlp.utn.edu.ar/login',
                },
            )
            # Enviar el correo en un hilo separado para no bloquear la respuesta
            thread = threading.Thread(target=email.send)
            thread.start()
        return redirect('staff_home')  # Redirige a la vista deseada
    else:
        return redirect('home')  # Redirige a la vista deseada


class InscriptosActividad(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = UserAsistente
    template_name = 'admin/actividad_inscriptos.html'
    context_object_name = 'asistentes'

    def test_func(self):
        return self.request.user.is_staff
    
    def get_queryset(self):
        # Suponiendo que la actividad tiene una clave primaria (pk) pasada por la URL
        actividad = Actividad.objects.get(pk=self.kwargs['actividad_id'])
        # Retornamos los asistentes de esa actividad
        return actividad.asistentes.all()

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        # Agregamos la actividad al contexto, si deseas mostrar más información
        context['actividad'] = Actividad.objects.get(pk=self.kwargs['actividad_id'])
        context['asistentes'] = Actividad.objects.get(pk=self.kwargs['actividad_id']).asistentes.all()
        return context


def envio_correos_entradas(request, actividad_id):
    if request.user.is_authenticated and request.user.is_staff:
        # Llamar al método save del formulario para obtener la instancia y la contraseña
        actividad = Actividad.objects.get(id=actividad_id)
        for asistente in actividad.asistentes.all():
            nombre = asistente.user.first_name
            correo = asistente.user.email
            dependencia = asistente.dependencia.nombre_largo
            username = asistente.user.username
            password = asistente.documento
    
            # Crear y enviar el correo
            email = create_email(
                user_mail=correo,
                subject='Confirmación de Inscripción al CNEISI',
                template_name='correos/inscripcion.html',
                context={
                    'usuario': username,  # Enviar el nombre de usuario
                    'nombre': nombre,  # Enviar el nombre del usuario
                    'dependencia': dependencia,
                    'password': password,
                    'url': 'https://cneisi.frlp.utn.edu.ar/login',
                },
            )
            # Enviar el correo en un hilo separado para no bloquear la respuesta
            thread = threading.Thread(target=email.send)
            thread.start()
        return redirect('staff_home')  # Redirige a la vista deseada
    else:
        return redirect('home')  # Redirige a la vista deseada
