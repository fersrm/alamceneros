from django.contrib import admin
from FacturasStoreApp.models import Facturas


class SharedModelAdminBase(admin.ModelAdmin):
    def has_module_permission(self, request):
        tenant_type = request.tenant.type
        allowed_tenant_types = ["type1", "type2"]
        return tenant_type in allowed_tenant_types


@admin.register(Facturas)
class FacturaAdmin(SharedModelAdminBase):
    list_display = ("id_factura", "total_factura")
