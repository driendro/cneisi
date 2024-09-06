from import_export import resources
from .models import UserAsistente, UserCoordinador


class AsistenteResource(resources.ModelResource):
    class Meta:
        model = UserAsistente
        fields = [
            'first_name',
            'last_name',
            'email',
            'documento',
            'cuit',
            'fecha_nacimiento',
            'telefono_personal',
            'telefono_emergencia',
            'dependencia',
            'grupo_sangineo',
            'regimen_comida',
            'regimen_comida_otro',
            'talle_ropa',
            'alergia',
            'alergia_otro',
            'medicamento',
            'medicamento_otro'
        ]

    def before_import(self, dataset, using_transactions=True):
        # Aquí puedes realizar acciones antes de importar los datos, como limpiar el dataset
        pass

    def after_import(self, dataset, result, using_transactions=True):
        # Aquí puedes realizar acciones después de importar los datos, como enviar notificaciones
        pass


class CoordinadorResource(resources.ModelResource):
    class Meta:
        model = UserCoordinador
