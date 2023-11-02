from django.contrib import admin
from .models import Cliente

# Clase base de administración con el método común


class SharedModelAdminBase(admin.ModelAdmin):
  def has_module_permission(self, request):
    tenant_type = request.tenant.type
    allowed_tenant_types = ['type2']  # Agrega los tipos permitidos
    return tenant_type in allowed_tenant_types

# -------------------------CLIENTE--------------------------


@admin.register(Cliente)
class ClienteAdmin(SharedModelAdminBase):
  list_display = (
      'id_cliente',
      'run_cliente',
      'nombre_cliente',
      'apellido_cliente',
      'telefono_cliente')
