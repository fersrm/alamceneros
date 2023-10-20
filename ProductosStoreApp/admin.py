from django.contrib import admin
from ProductosStoreApp.models import Marca, Producto, Categoria

# para borrar imagenes
from django.dispatch import receiver
from django.db.models.signals import post_delete

# Register your models here.


admin.site.register(Marca)
admin.site.register(Categoria)
# Register your models here.

# -----------------PRODUCTOS--------------------------------------------


class ProducAdmin(admin.ModelAdmin):
  readonly_fields = ('fecha',)

  def marca(self, obj):
    return getattr(obj, 'marca_FK')
  marca.short_description = 'Marca'

  def categoria(self, obj):
    return getattr(obj, 'categoria_FK')
  categoria.short_description = 'Categoria'
  list_display = (
      'id_producto',
      'codigo_producto',
      'nombre_producto',
      'precio_producto',
      'marca',
      'categoria')


admin.site.register(Producto, ProducAdmin)


@receiver(post_delete, sender=Producto)
def eliminar_imagen_producto(sender, instance, **kwargs):
  instance.imagen.delete(save=False)
