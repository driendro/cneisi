from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
from .models import UserAsistente, UserCoordinador, Dependencia, Aula, Actividad, TallesRemeras
# Register your models here.

admin.site.register(UserCoordinador)
admin.site.register(UserAsistente)
admin.site.register(TallesRemeras)
admin.site.register(Dependencia)
admin.site.register(Aula)
admin.site.register(Actividad)
