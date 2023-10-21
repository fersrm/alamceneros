from django.contrib import admin
from DatosEmpresaStoreApp.models import DatosEmpresa


class SharedModelAdminBase(admin.ModelAdmin):
  def has_module_permission(self, request):
    tenant_type = request.tenant.type
    allowed_tenant_types = ['type1', 'type2']
    return tenant_type in allowed_tenant_types

# Registro de DatosEmpresa


@admin.register(DatosEmpresa)
class DatosEmpresaAdmin(SharedModelAdminBase):
  list_display = ('id_datos_empresa', 'nombre_empresa')
