# Generated by Django 4.2.16 on 2024-10-16 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0018_remove_mazo_cartas_alter_cartamazo_carta'),
        ('Battle', '0002_alter_jugadorbatalla_unique_together'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ReservaTurnoJugador',
            new_name='ReservaJugador',
        ),
        migrations.AlterField(
            model_name='batalla',
            name='nombre',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='turno',
            name='turno',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='turno',
            unique_together={('batalla', 'turno')},
        ),
        migrations.CreateModel(
            name='CartaActivaJugador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batalla', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Battle.batalla')),
                ('carta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.cartamazo')),
                ('jugador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Battle.jugadorbatalla')),
                ('turno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Battle.turno')),
            ],
        ),
    ]
