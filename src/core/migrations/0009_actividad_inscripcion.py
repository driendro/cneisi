# Generated by Django 5.1.1 on 2024-09-18 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_actividad_habilitada'),
    ]

    operations = [
        migrations.AddField(
            model_name='actividad',
            name='inscripcion',
            field=models.BooleanField(default=False),
        ),
    ]