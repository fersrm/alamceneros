from django.contrib import admin
from ProductosStoreApp.models import Marca, Producto, Categoria

# para borrar imagenes
from django.dispatch import receiver
from django.db.models.signals import post_delete

# -----------------PRODUCTOS----------------


class SharedModelAdminBase(admin.ModelAdmin):
  def has_module_permission(self, request):
    tenant_type = request.tenant.type
    allowed_tenant_types = ['type1', 'type2']
    return tenant_type in allowed_tenant_types

# Registro de Marca


@admin.register(Marca)
class MarcaAdmin(SharedModelAdminBase):
  pass

# Registro de Categoria


@admin.register(Categoria)
class CategoriaAdmin(SharedModelAdminBase):
  pass

# Registro de Producto


@admin.register(Producto)
class ProductoAdmin(SharedModelAdminBase):
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


@receiver(post_delete, sender=Producto)
def eliminar_imagen_producto(sender, instance, **kwargs):
  instance.imagen.delete(save=False)
