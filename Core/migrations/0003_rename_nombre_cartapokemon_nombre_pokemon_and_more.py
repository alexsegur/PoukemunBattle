# Generated by Django 4.2.16 on 2024-10-09 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0002_alter_coleccion_ataque_delete_entrenadorpokemon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartapokemon',
            old_name='nombre',
            new_name='nombre_pokemon',
        ),
        migrations.AddField(
            model_name='cartapokemon',
            name='apodo',
            field=models.CharField(default='', max_length=50),
        ),
    ]
