from django.db import models
# son para borrar imagen al actualizar
import os
from django.dispatch import receiver
from django.db.models.signals import pre_save
from UsuariosStoreApp.models import Usuario
from django.conf import settings
# Create your models here.


def dynamic_upload_path(instance, filename):
  return "productos/{}".format(filename)


# -----------------------Productos----------------


class Marca(models.Model):
  id_marca = models.AutoField(primary_key=True)
  nombre_marca = models.CharField(max_length=45, unique=True)

  class Meta:
    db_table = 'marca'

  def __str__(self):
    return f"{self.nombre_marca}"


class Categoria(models.Model):
  id_categoria = models.AutoField(primary_key=True)
  nombre_categoria = models.CharField(max_length=45, unique=True)

  class Meta:
    db_table = 'categoria'

  def __str__(self):
    return f"{self.nombre_categoria}"


class Producto(models.Model):
  id_producto = models.AutoField(primary_key=True)
  codigo_producto = models.CharField(max_length=45, unique=True)
  nombre_producto = models.CharField(max_length=45)
  precio_producto = models.IntegerField()
  imagen = models.ImageField(upload_to=dynamic_upload_path)
  stock = models.IntegerField(default=10)
  fecha = models.DateField(auto_now_add=True)
  marca_FK = models.ForeignKey(Marca, on_delete=models.CASCADE)
  usuario_FK = models.ForeignKey(Usuario, on_delete=models.CASCADE)
  # usuario_FK = models.IntegerField()
  categoria_FK = models.ForeignKey(Categoria, on_delete=models.CASCADE)

  class Meta:
    db_table = 'producto'

  def __str__(self):
    return f"{self.nombre_producto}"

  def borrar_imagen_anterior(self):
    if self.id_producto is not None:
      try:
        producto_anterior = Producto.objects.get(id_producto=self.id_producto)
        if producto_anterior.imagen != self.imagen:
          ruta_img = os.path.abspath(producto_anterior.imagen.path)
          if os.path.exists(ruta_img):
            os.remove(ruta_img)
      except Producto.DoesNotExist as e:
        print(f"Producto con id {self.id_producto} no funciona: {e}")


@receiver(pre_save, sender=Producto)
def borrar_imagen_anterior(sender, instance, **kwargs):
  instance.borrar_imagen_anterior()
