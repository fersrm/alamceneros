from django.contrib import admin
from .models import Cliente, Region, Comuna

# Clase base de administración con el método común


class SharedModelAdminBase(admin.ModelAdmin):
  def has_module_permission(self, request):
    tenant_type = request.tenant.type
    allowed_tenant_types = ['type2']  # Agrega los tipos permitidos
    return tenant_type in allowed_tenant_types

# Registro de Comuna


@admin.register(Comuna)
class ComunaAdmin(SharedModelAdminBase):
  pass

# Registro de Region


@admin.register(Region)
class RegionAdmin(SharedModelAdminBase):
  pass

# -------------------------CLIENTE--------------------------


@admin.register(Cliente)
class ClienteAdmin(SharedModelAdminBase):
  def comuna(self, obj):
    return getattr(obj, 'comuna_FK')
  comuna.short_description = 'Comuna'
  list_display = (
      'id_cliente',
      'run_cliente',
      'nombre_cliente',
      'apellido_cliente',
      'comuna')
