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
    
class UserAsistenteAdmin(admin.ModelAdmin):
    # Lista los campos que se mostrarán en el listado del admin en formato tabla
    list_display = ('user__last_name', 'user__first_name', 'user__email', 'documento', 'dependencia__nombre_corto')

    # Opcional: Añade búsqueda por los campos que desees
    search_fields = ('user__last_name', 'user__first_name', 'user__email', 'documento', 'dependencia__nombre_corto', 'dependencia__nombre_largo')

    # Opcional: Filtrado por año u otro campo
    list_filter = ('dependencia__nombre_corto','talle_ropa__designacion')


admin.site.register(UserCoordinador)
admin.site.register(UserAsistente, UserAsistenteAdmin)
admin.site.register(TallesRemeras)
admin.site.register(Dependencia)
admin.site.register(Aula)
admin.site.register(Sponsors)
admin.site.register(Actividad, ActividadAdmin)
