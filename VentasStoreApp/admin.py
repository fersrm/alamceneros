from django.contrib import admin
from VentasStoreApp.models import Boletas, Ventas

# Clase base de administración con el método común


class SharedModelAdminBase(admin.ModelAdmin):
    def has_module_permission(self, request):
        tenant_type = request.tenant.type
        allowed_tenant_types = ["type1", "type2"]
        return tenant_type in allowed_tenant_types


# Registro de Boletas


@admin.register(Boletas)
class BoletasAdmin(SharedModelAdminBase):
    list_display = ("id_boleta", "total_boleta")


# Registro de Ventas


@admin.register(Ventas)
class VentasAdmin(SharedModelAdminBase):
    list_display = ("id_venta", "fecha_emision", "usuario_FK")
