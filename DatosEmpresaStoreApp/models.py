from django.db import models

# Create your models here.


class DatosEmpresa(models.Model):
  id_datos_empresa = models.AutoField(primary_key=True)
  nombre_empresa = models.CharField(max_length=45)
  rut_empresa = models.CharField(max_length=15)
  email = models.CharField(max_length=64, default='pepe@gmail.com')
  telefono = models.CharField(max_length=15, default='123456789')
  comuna = models.CharField(max_length=45, default='Chillan')
  direccion_empresa = models.CharField(max_length=45)
  IVA = models.IntegerField()

  class Meta:
    db_table = 'datosempresa'

  def __str__(self):
    return f"{self.nombre_empresa}"
