# Generated by Django 4.2.9 on 2024-01-30 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sense', '0004_sensorfigure'),
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensormonitor',
            name='sensor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='monitor', to='sense.sensor', verbose_name='سنسور مربوطه'),
        ),
    ]
