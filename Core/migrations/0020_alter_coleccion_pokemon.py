# Generated by Django 5.1.1 on 2024-10-16 18:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0019_set_cartapokemon_rare_boosterpack_cartapokemon_set'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coleccion',
            name='pokemon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemons_coleccionados', to='Core.cartapokemon'),
        ),
    ]
