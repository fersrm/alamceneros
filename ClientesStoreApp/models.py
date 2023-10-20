from django.db import models
from .choices import tipoGiro

# Create your models here.


class Region(models.Model):
  id_regiones = models.AutoField(primary_key=True)
  nombre_region = models.CharField(max_length=45, unique=True)

  class Meta:
    db_table = 'region'

  def __str__(self):
    return f"{self.nombre_region}"


class Comuna(models.Model):
  id_comuna = models.AutoField(primary_key=True)
  nombre_comuna = models.CharField(max_length=45, unique=True)
  region_FK = models.ForeignKey(Region, on_delete=models.CASCADE)

  class Meta:
    db_table = 'comuna'

  def __str__(self):
    return f"{self.nombre_comuna}"


class Cliente(models.Model):
  id_cliente = models.AutoField(primary_key=True)
  run_cliente = models.CharField(max_length=15, unique=True)
  nombre_cliente = models.CharField(max_length=45)
  apellido_cliente = models.CharField(max_length=45)
  correo_cliente = models.CharField(max_length=64, unique=True)
  razon_social = models.CharField(max_length=45)
  direccion = models.CharField(max_length=45)
  tipo_giro = models.IntegerField(choices=tipoGiro, default=2)
  comuna_FK = models.ForeignKey(Comuna, on_delete=models.CASCADE)

  class Meta:
    db_table = 'cliente'

  def __str__(self):
    return f"{self.nombre_cliente} {self.apellido_cliente}"
