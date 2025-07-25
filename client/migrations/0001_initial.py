# Generated by Django 5.1.4 on 2025-06-19 16:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Azulejo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(blank=True, default='', max_length=100)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='client/static/img/azulejos')),
                ('latitud', models.DecimalField(decimal_places=6, default=0, max_digits=9, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)])),
                ('longitud', models.DecimalField(decimal_places=6, default=0, max_digits=9, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
                ('nombre', models.CharField(blank=True, default='', max_length=100, verbose_name='Nombre')),
                ('descripcion', models.TextField(blank=True, default='', verbose_name='Descripción')),
                ('estilo', models.CharField(blank=True, choices=[('COL', 'Colonial'), ('BAR', 'Barroco'), ('NEO', 'Neoclásico'), ('ART', 'Art Nouveau'), ('DEC', 'Art Déco'), ('MOD', 'Moderno'), ('CON', 'Contemporáneo')], default='', max_length=3, verbose_name='Estilo')),
                ('epoca', models.CharField(blank=True, default='', max_length=50, verbose_name='Época')),
                ('ubicacion', models.CharField(blank=True, default='', max_length=200, verbose_name='Ubicación')),
                ('imagen_principal', models.ImageField(blank=True, default='', upload_to='catalogo/', verbose_name='Imagen principal')),
                ('imagen_detalle', models.ImageField(blank=True, null=True, upload_to='catalogo/', verbose_name='Imagen detalle')),
                ('coleccion', models.CharField(blank=True, max_length=100, verbose_name='Colección')),
            ],
            options={
                'verbose_name': 'Ubicación de Azulejo',
                'verbose_name_plural': 'Ubicaciones de Azulejos',
            },
        ),
    ]
