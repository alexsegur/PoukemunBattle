# Generated by Django 4.2.16 on 2024-10-11 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0014_alter_mazoentrenador_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mazoentrenador',
            name='nombre',
            field=models.CharField(default='', max_length=50),
        ),
    ]