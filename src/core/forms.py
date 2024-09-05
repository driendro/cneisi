from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Usuarios, Dependencia, Aula, Actividad, TallesRemeras


class UsuariosForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = (
            'documento',
            'cuit',
            'fecha_nacimiento',
            'telefono_personal',
            'telefono_emergencia',
            'caracter',
            'dependencia',
            'grupo_sangineo',
            'regimen_comida',
            'regimen_comida_otro',
            'talle_ropa',
            'alergia',
            'alergia_otro',
            'medicamento',
            'medicamento_otro'
        )

    # Add a field for the Django user's username and password
    first_name = forms.CharField(label='Nombre')
    last_name = forms.CharField(label='Apellido')
    email = forms.CharField(label='Correo Electronico')
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), label='Password')

    def clean_documento(self):
        documento = self.cleaned_data['documento']
        if Usuarios.objects.filter(documento=documento).exists():
            raise forms.ValidationError('Ese numero de Documento ya existe.')
        return documento

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['documento'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        instance = super().save(commit=False)
        instance.user = user
        instance.save()
        return instance