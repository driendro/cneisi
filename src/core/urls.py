"""
URL configuration for cneisi project.

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
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from core.views import (
    EliminarInscriptoActividad,
    EditarAsistenteAdmin,
    PerfilHome,
    InscriptosList,
    UsuariosCreateView,
    import_users,
    EliminarAsistente,
    EditarAsistente,
    DetalleAsistente,
    AsistenteHome,
    inscribirse,
    desinscribirse,
    StaffHome,
    abir_inscripciones,
    cerrar_inscripciones,
    envio_correos_inscripcion,
    envio_correos_entradas,
    InscriptosActividad
)

urlpatterns = [
    
    #Coordinador###################################################################
    path('home', PerfilHome.as_view(), name='perfil_home'),
    path('coordinador/home', InscriptosList.as_view(), name='coordinador_home'),
    path('coordinador/inscribir_uno', UsuariosCreateView.as_view(),
         name='coordinador_inscribir_uno'),
    path('coordinador/inscribir_muchos', import_users,
         name='coordinador_inscribir_muchos'),
    path('coordinador/user/<int:pk>/editar', EditarAsistente.as_view(),
         name='coordinador_editar_asistente'),
    path('coordinador/user/<int:pk>/eliminar', EliminarAsistente.as_view(),
         name='coordinador_eliminar_asistente'),
    path('coordinador/user/<int:pk>/ver', DetalleAsistente.as_view(),
         name='coordinador_ver_asistente'),
    
    #Asistente###################################################################
    path('asistente', AsistenteHome.as_view(), name='asistente_home'),
    path('inscribirse/<int:actividad_id>/',
         inscribirse, name='actividad_inscribirse'),
    path('desinscribirse/<int:actividad_id>/',
         desinscribirse, name='actividad_desinscribirse'),
    
    #Admin_Staff###################################################################
    path('admin', StaffHome.as_view(), name='staff_home'),
    path('admin/abrir_inscripciones',
         abir_inscripciones, name='abrir_inscripciones'),
    path('admin/cerrar_inscripciones', cerrar_inscripciones, name='cerrar_inscripciones'),
    path('admin/enviar_correo', envio_correos_inscripcion, name='enviar_correos'),
    path('admin/ver_inscriptos/<int:actividad_id>',
         InscriptosActividad.as_view(), name='ver_inscriptos'),
    
    path('admin/user/<int:pk>/ver', DetalleAsistente.as_view(),
         name='admin_ver_asistente'),

    path('admin/<int:pk>/eliminar/<int:actividad_id>/', EliminarInscriptoActividad.as_view(),
         name='admin_eliminar_inscripto_actividad'),

    path('admin/user/<int:pk>/editar/<int:actividad_id>/', EditarAsistenteAdmin.as_view(),
         name='admin_editar_asistente')
]
