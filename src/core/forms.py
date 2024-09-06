from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import UserAsistente
import random
import string


def generar_cadena_alternante():
  """Genera una cadena aleatoria de 6 caracteres, alternando números y letras."""

  numeros = ''.join(random.choice(string.digits) for _ in range(3))
  letras = ''.join(random.choice(string.ascii_lowercase) for _ in range(3))

  return numeros + letras

class UsuariosForm(forms.ModelForm):
    # Add a field for the Django user's username and password
    first_name = forms.CharField(label='Nombre')
    last_name = forms.CharField(label='Apellido')
    email = forms.CharField(label='Correo Electronico')
    #password = forms.CharField(widget=forms.PasswordInput(render_value=False), label='Password')

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
            #'caracter',
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
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electronico',
            'documento': 'Numero de documento',
            'cuit': 'Numero de cuit (sin guiones)',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'telefono_personal': 'Telefono Personal (de la forma +541223456789)',
            'telefono_emergencia': 'Telefono de emergencia (de la forma +541223456789)',
            #'caracter': 'En ca',
            'dependencia': 'Dependencia e',
            'grupo_sangineo': 'Grupo y Factor sanguineo',
            'regimen_comida': 'Regimen alimenticio',
            'regimen_comida_otro': 'Si repondio "Otros", explique:',
            'talle_ropa': 'Talle de Remera',
            'alergia': '¿Sufre de alguna alergia?',
            'alergia_otro': '¿Cual?',
            'medicamento': '¿Consume algun medicamento de forma regular?',
            'medicamento_otro': '¿Cual?'
        }
        help_texts = {
        }
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={
                'type': 'date', 'placeholder': 'dd-mm-yyyy (DOB)', 'class': 'form-control'}
            ),
            #'dependencia': forms.RadioSelect(attrs={
            #    'type': 'select', 'class': 'form-control'}
            #),
            'regimen_comida_otro': forms.Textarea(attrs={
                'type': 'text', 'class': 'form-control'}
            ),
            'alergia_otro': forms.Textarea(attrs={
                'type': 'text', 'class': 'form-control'}
            ),
            'medicamento_otro': forms.Textarea(attrs={
                'type': 'text', 'class': 'form-control'}
            )
        }
    
    def clean_caracter(self):
        caracter = 'Asistente'
        return caracter

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['documento'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=str(generar_cadena_alternante())
        )
        instance = super().save(commit=False)
        instance.user = user
        instance.save()
        return instance

