from django.db import models

# son para borrar imagen al actualizar
from ClientesStoreApp.models import Cliente
from ProductosStoreApp.models import Producto
from VentasStoreApp.models import Ventas


# Create your models here.


class Facturas(models.Model):
    id_factura = models.AutoField(primary_key=True)
    total_factura = models.IntegerField()
    cliente_fk = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    venta_FK = models.ForeignKey(Ventas, on_delete=models.CASCADE)

    class Meta:
        db_table = "facturas"

    def __str__(self):
        return f"{self.id_factura}"


class DetalleFacturas(models.Model):
    id_detalle_factura = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    total = models.IntegerField()
    producto_FK = models.ForeignKey(Producto, on_delete=models.CASCADE)
    factura_FK = models.ForeignKey(Facturas, on_delete=models.CASCADE)

    class Meta:
        db_table = "detallefactura"

    def __str__(self):
        return f"{self.id_detalle_factura}"
