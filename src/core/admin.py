from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
from .models import UserAsistente, UserCoordinador, Dependencia, Aula, Actividad, TallesRemeras, Sponsors
# Register your models here.


class ActividadAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None,
            {"fields": ['tipo', 'nombre', 'descripcion', 'fecha', 'hora_inicio', 'hora_final', 'orador', 'aula', 'portada', 'inscripcion'],},
        ),
        (
            "Avanzada",
            {
                "classes": ["collapse"],
                "fields": ["habilitada"],
            },
        ),
    ]

admin.site.register(UserCoordinador)
admin.site.register(UserAsistente)
admin.site.register(TallesRemeras)
admin.site.register(Dependencia)
admin.site.register(Aula)
admin.site.register(Sponsors)
admin.site.register(Actividad, ActividadAdmin)
