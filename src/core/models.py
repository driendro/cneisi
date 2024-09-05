from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User

CARACTER_CHOICES = {
    'asistente': 'Asistente',
    'coordinador': 'Coordinador',
    'chofer': 'Chofer',
}

GRUPO_FACTOR_CHOICES = {
    'a+': 'A (+)',
    'b+': 'B (+)',
    'ab+': 'AB (+)',
    'o+': 'O (+)',
    'a-': 'A (-)',
    'b-': 'B (-)',
    'ab-': 'AB (-)',
    'o-': 'O (-)'
}

REGIMEN_COMIDA_CHOICES = {
    'ninguno': 'Sin Restricciones',
    'vegetariano': 'Vegetariano',
    'celiaco': 'Celiaco',
    'vegano': 'Vegano',
    'otros': 'Otros'
}

# Create your models here.
class Dependencia(models.Model):
    nombre_largo = models.CharField(max_length=100)
    nombre_corto = models.CharField(max_length=10)
    cupo = models.IntegerField()
    
    def __str__(self):
        return self.nombre_corto.upper()


class TallesRemeras(models.Model):
    designacion = models.CharField(max_length=5)
    alto = models.FloatField()
    ancho = models.FloatField()

    def __str__(self):
        return '{} ({}x{} cm)'.format(self.designacion.upper(), self.alto, self.ancho)


class Usuarios(models.Model):
    user = models.OneToOneField(User, related_name='UserUsuario', on_delete=models.CASCADE)
    documento = models.IntegerField(unique=True)
    cuit = models.IntegerField()
    fecha_nacimiento = models.DateField()
    telefono_personal = PhoneNumberField()
    telefono_emergencia = PhoneNumberField()
    caracter = models.CharField(max_length=15, choices=CARACTER_CHOICES)
    dependencia = models.ManyToManyField('Dependencia', related_name='dependencia')
    grupo_sangineo = models.CharField(max_length=4, choices=GRUPO_FACTOR_CHOICES)
    regimen_comida = models.CharField(max_length=15, choices=REGIMEN_COMIDA_CHOICES)
    regimen_comida_otro = models.TextField(blank=True, null=True)
    talle_ropa = models.ForeignKey('TallesRemeras', related_name='talle_remera', on_delete=models.CASCADE)
    alergia = models.CharField(max_length=2, choices={'si': 'Si', 'no': 'No'})
    alergia_otro = models.TextField(blank=True, null=True)
    medicamento = models.CharField(max_length=2, choices={'si': 'Si', 'no': 'No'})
    medicamento_otro = models.TextField(blank=True, null=True)

    # Otros métodos personalizados si es necesario
    def __str__(self):
        return '{}, {}'.format(self.user.last_name.upper(), self.user.first_name.title())


class Aula(models.Model):
    nombre = models.CharField(max_length=20)
    cupo = models.IntegerField()
    
    def __str__(self):
        return '{} ({})'.format(self.nombre.upper(), self.cupo)


class Actividad(models.Model):
    tipo = models.CharField(max_length=150)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    orador = models.CharField(max_length=100)
    aula = models.ForeignKey('Aula', related_name='AulaActividad', on_delete=models.CASCADE)
