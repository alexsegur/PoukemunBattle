# Generated by Django 4.2.16 on 2024-10-16 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0018_remove_mazo_cartas_alter_cartamazo_carta'),
        ('Battle', '0003_rename_reservaturnojugador_reservajugador_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='descartesjugador',
            name='carta',
        ),
        migrations.RemoveField(
            model_name='manojugador',
            name='carta',
        ),
        migrations.RemoveField(
            model_name='reservajugador',
            name='carta',
        ),
        migrations.CreateModel(
            name='CartaReservaJugador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.cartamazo')),
                ('reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Battle.reservajugador')),
            ],
        ),
        migrations.CreateModel(
            name='CartaManoJugador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.cartamazo')),
                ('mano', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Battle.manojugador')),
            ],
        ),
        migrations.CreateModel(
            name='CartaDescartesJugador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.cartamazo')),
                ('descarte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Battle.descartesjugador')),
            ],
        ),
    ]