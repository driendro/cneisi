from datetime import date
import os
from uuid import uuid4
from django.forms import ValidationError
from django.utils.text import slugify
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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    documento = models.IntegerField(unique=True)
    cuit = models.PositiveBigIntegerField()
    fecha_nacimiento = models.DateField()
    telefono_personal = PhoneNumberField()
    telefono_emergencia = PhoneNumberField()
    caracter = models.CharField(
        max_length=15, choices=CARACTER_CHOICES, default='asistente')
    grupo_sangineo = models.CharField(max_length=4, choices=GRUPO_FACTOR_CHOICES)
    regimen_comida = models.CharField(max_length=15, choices=REGIMEN_COMIDA_CHOICES)
    regimen_comida_otro = models.TextField(blank=True, null=True)
    talle_ropa = models.ForeignKey('TallesRemeras', on_delete=models.CASCADE)
    alergia = models.CharField(max_length=2, choices={'si': 'Si', 'no': 'No'})
    alergia_otro = models.TextField(blank=True, null=True)
    medicamento = models.CharField(max_length=2, choices={'si': 'Si', 'no': 'No'})
    medicamento_otro = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class UserAsistente(Usuarios):
    dependencia = models.ForeignKey(
        'Dependencia', on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        # Eliminar el usuario asociado antes de eliminar el asistente
        self.user.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return '{}, {}'.format(self.user.last_name.upper(), self.user.first_name.title())

    class Meta:
        managed = True
        verbose_name = 'Asistente'
        verbose_name_plural = 'Asistentes'


class UserCoordinador(Usuarios):
    dependencia = models.ManyToManyField('Dependencia')

    def delete(self, *args, **kwargs):
        # Eliminar el usuario asociado antes de eliminar el asistente
        self.user.delete()
        super().delete(*args, **kwargs)
        
    def __str__(self):
        return '{}, {}'.format(self.user.last_name.upper(), self.user.first_name.title())

    class Meta:
        managed = True
        verbose_name = 'Coordinador'
        verbose_name_plural = 'Coordinadores'


class Aula(models.Model):
    nombre = models.CharField(max_length=20)
    cupo = models.IntegerField(default=0)  # 0 significa que no hay límite

    def __str__(self):
        return '{} ({})'.format(self.nombre.upper(), "Ilimitado" if self.cupo == 0 else self.cupo)


def generar_ruta_unica(instance, filename):
    # Extraer la extensión del archivo
    ext = filename.split('.')[-1]
    # Crear un nombre de archivo único usando UUID
    filename = '{}.{}'.format(uuid4(),ext)
    # Generar una carpeta con el tipo y nombre de la actividad
    actividad_nombre = slugify(instance.nombre)
    # Devolver la ruta completa donde se almacenará la imagen
    return os.path.join('portadas', actividad_nombre, filename)

class Actividad(models.Model):
    tipo = models.CharField(max_length=150)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    hora_inicio = models.TimeField(default='00:00')
    hora_final = models.TimeField(default='00:00')
    orador = models.CharField(max_length=100)
    aula = models.ForeignKey('Aula', related_name='AulaActividad', on_delete=models.CASCADE)
    portada = models.ImageField(upload_to=generar_ruta_unica, default='#')
    asistentes = models.ManyToManyField(UserAsistente, blank=True)
    
    def __str__(self):
        return '{} ({})'.format(self.nombre.upper(), self.aula.nombre)

    def inscribir_asistente(self, user_asistente):
        # Verificar si el aula tiene cupo limitado
        if self.aula.cupo > 0:
            # Contar los asistentes ya inscritos
            inscritos = self.asistentes.count()
            if inscritos >= self.aula.cupo:
                # Si el número de inscritos es mayor o igual al cupo, lanzar una excepción
                raise ValidationError('El cupo máximo de esta actividad ha sido alcanzado.')

        # Agregar el asistente si el cupo no ha sido alcanzado o es ilimitado (0)
        self.asistentes.add(user_asistente)

    def cupo_disponible(self):
        # Si el cupo es 0, significa que es ilimitado
        if self.aula.cupo == 0:
            return "Cupo ilimitado"
        else:
            # Devolver el número de lugares restantes
            return self.aula.cupo - self.asistente.count()