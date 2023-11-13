from django.db import models
from .choices import tipoDoc, tipoImpuesto
from ProveedoresStoreApp.models import Proveedor

# Create your models here.


class Compras(models.Model):
    id_compras = models.AutoField(primary_key=True)
    num_documento = models.CharField(max_length=15, unique=True)
    fecha = models.DateField()
    total = models.IntegerField()
    tipo_documento = models.IntegerField(choices=tipoDoc, default=1)
    tipo_impuesto = models.IntegerField(choices=tipoImpuesto, default=1)
    proveedor_FK = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    class Meta:
        db_table = "compras"

    def __str__(self):
        return f"{self.num_documento}"
