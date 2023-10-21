# Generated by Django 4.2.6 on 2023-10-20 23:08

import ProductosStoreApp.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id_categoria', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_categoria', models.CharField(max_length=45, unique=True)),
            ],
            options={
                'db_table': 'categoria',
            },
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id_marca', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_marca', models.CharField(max_length=45, unique=True)),
            ],
            options={
                'db_table': 'marca',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.AutoField(primary_key=True, serialize=False)),
                ('codigo_producto', models.CharField(max_length=45, unique=True)),
                ('nombre_producto', models.CharField(max_length=45)),
                ('precio_producto', models.IntegerField()),
                ('imagen', models.ImageField(upload_to=ProductosStoreApp.models.dynamic_upload_path)),
                ('stock', models.IntegerField(default=10)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('categoria_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProductosStoreApp.categoria')),
                ('marca_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProductosStoreApp.marca')),
            ],
            options={
                'db_table': 'producto',
            },
        ),
    ]