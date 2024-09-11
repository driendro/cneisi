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
from django.urls import path
from django.views.generic import TemplateView
import core.views_publics as vp 



urlpatterns = [
    path('', TemplateView.as_view(template_name="landing/home.html"), name='home'),
    path('ejes_tematicos', TemplateView.as_view(template_name="landing_vieja/home.html"), name='trabajos_ejes'),
    #path('', TemplateView.as_view(), name='trabajos_fechas'),
    #path('', TemplateView.as_view(), name='trabajos_envio'),
    #path('', TemplateView.as_view(), name='inscripcion'),
    #path('', TemplateView.as_view(), name='conferencias'),
    #path('', TemplateView.as_view(), name='evento_general'),
    #path('', TemplateView.as_view(), name='evento_actividades'),
    #path('', TemplateView.as_view(), name='certificado'),
    #path('', TemplateView.as_view(), name='contacto'),
    #path('', TemplateView.as_view(), name='circulares'),
]
