# Generated by Django 4.2.4 on 2023-11-03 01:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Giro',
            fields=[
                ('id_giro', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_giro', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'giro',
            },
        ),
        migrations.CreateModel(
            name='Rubro',
            fields=[
                ('id_rubro', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_rubro', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'rubro',
            },
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id_proveedor', models.AutoField(primary_key=True, serialize=False)),
                ('run_proveedor', models.CharField(max_length=15, unique=True)),
                ('nombre_proveedor', models.CharField(max_length=45)),
                ('razon_social', models.CharField(max_length=45)),
                ('correo_proveedor', models.CharField(max_length=64, unique=True)),
                ('telefono_proveedor', models.CharField(max_length=45)),
                ('contacto', models.CharField(max_length=45)),
                ('direccion', models.CharField(max_length=45)),
                ('giro_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProveedoresStoreApp.giro')),
                ('rubro_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProveedoresStoreApp.rubro')),
            ],
            options={
                'db_table': 'proveedor',
            },
        ),
    ]
