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
from django.conf.urls import include
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('core.urls')),
    path('', include('core.urls_publics')),
        
    #Urls de administracion de cuenta
    path("cuentas/login/", auth_views.LoginView.as_view(template_name="cuentas/login.html"), name='login'),
    path("cuentas/logout/", auth_views.LogoutView.as_view(template_name="cuentas/logout.html"), name='logout'),
    # path("cuentas/password_change/", auth_views.PasswordChangeView.as_view(template_name="cuentas/password_change.html"), name='password_change'),
    # path("cuentas/password_change/done/", auth_views.PasswordChangeDoneView.as_view(template_name="cuentas/password_change_done.html"), name='password_change_done'),
    path("cuentas/password_reset/", auth_views.PasswordResetView.as_view(template_name="cuentas/password_reset_form.html"), name='password_reset'),
    path("cuentas/password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="cuentas/password_reset_done.html"), name='password_reset_done'),
    path("cuentas/reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="cuentas/password_reset_confirm.html"), name='password_reset_confirm'),
    path("cuentas/reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="cuentas/password_reset_complete.html"), name='password_reset_complete')
]

# Solo necesario en desarrollo, no en producción.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
