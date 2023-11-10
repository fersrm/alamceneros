from django.db import models

# son para borrar imagen al actualizar
from UsuariosStoreApp.models import Usuario
from ProductosStoreApp.models import Producto

# Create your models here.


class Ventas(models.Model):
    id_venta = models.AutoField(primary_key=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    usuario_FK = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    # usuario_FK = models.IntegerField()

    class Meta:
        db_table = "ventas"


class Boletas(models.Model):
    id_boleta = models.AutoField(primary_key=True)
    total_boleta = models.IntegerField()
    venta_FK = models.ForeignKey(Ventas, on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = "boletas"

    def __str__(self):
        return f"{self.id_boleta}"


class DetalleBoletas(models.Model):
    id_detalle_boleta = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    total = models.IntegerField()
    producto_FK = models.ForeignKey(Producto, on_delete=models.CASCADE)
    # producto_FK = models.IntegerField()
    boleta_FK = models.ForeignKey(Boletas, on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = "detalleboleta"

    def __str__(self):
        return f"{self.id_detalle_boleta}"
