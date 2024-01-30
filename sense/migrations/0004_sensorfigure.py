# Generated by Django 4.2.9 on 2024-01-30 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sense', '0003_alter_lightintensitysensor_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorFigure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='', verbose_name='فایل نمودار')),
                ('sensor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='figure', to='sense.sensor', verbose_name='سنسور مربوطه')),
            ],
            options={
                'verbose_name': 'نمودار سنسور',
                'verbose_name_plural': 'نمودارهای سنسور',
            },
        ),
    ]
