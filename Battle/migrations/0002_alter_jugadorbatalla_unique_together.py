# Generated by Django 4.2.16 on 2024-10-16 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0018_remove_mazo_cartas_alter_cartamazo_carta'),
        ('Battle', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='jugadorbatalla',
            unique_together={('batalla', 'jugador', 'mazo')},
        ),
    ]
