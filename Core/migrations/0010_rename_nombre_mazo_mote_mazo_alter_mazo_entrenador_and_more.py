# Generated by Django 4.2.16 on 2024-10-10 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0009_remove_mazo_pokemon_mazo_pokemon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mazo',
            old_name='nombre',
            new_name='mote_mazo',
        ),
        migrations.AlterField(
            model_name='mazo',
            name='entrenador',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mazo_del_entrenador', to='Core.jugadorentrenador'),
        ),
        migrations.RemoveField(
            model_name='mazo',
            name='pokemon',
        ),
        migrations.AddField(
            model_name='mazo',
            name='pokemon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pokemons_del_mazo', to='Core.cartapokemonataque'),
        ),
    ]
