# Generated by Django 4.2.16 on 2024-10-16 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Battle', '0004_remove_descartesjugador_carta_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turnojugador',
            name='activo',
        ),
        migrations.AddField(
            model_name='turnojugador',
            name='batalla',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Battle.batalla'),
        ),
        migrations.AlterField(
            model_name='cartaactivajugador',
            name='turno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Battle.turnojugador'),
        ),
    ]
