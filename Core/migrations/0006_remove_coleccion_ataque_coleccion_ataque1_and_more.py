# Generated by Django 4.2.16 on 2024-10-09 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0005_remove_cartapokemon_apodo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coleccion',
            name='ataque',
        ),
        migrations.AddField(
            model_name='coleccion',
            name='ataque1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ataque_debil', to='Core.cartapokemonataque'),
        ),
        migrations.AddField(
            model_name='coleccion',
            name='ataque2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ataque_fuerte', to='Core.cartapokemonataque'),
        ),
    ]
