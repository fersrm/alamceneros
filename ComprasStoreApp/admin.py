from django.contrib import admin
from .models import Compras

# Clase base de administración con el método común


class SharedModelAdminBase(admin.ModelAdmin):
  def has_module_permission(self, request):
    tenant_type = request.tenant.type
    allowed_tenant_types = ['type1', 'type2']  # Agrega los tipos permitidos
    return tenant_type in allowed_tenant_types

# -------------------------COMPRAS-------------------------


@admin.register(Compras)
class ComprasAdmin(SharedModelAdminBase):
  list_display = (
      'id_compras',
      'num_documento',)
