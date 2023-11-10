from django.contrib import admin
from .models import Proveedor, Giro, Rubro

# Clase base de administración con el método común


class SharedModelAdminBase(admin.ModelAdmin):
    def has_module_permission(self, request):
        tenant_type = request.tenant.type
        allowed_tenant_types = ["type1", "type2"]  # Agrega los tipos permitidos
        return tenant_type in allowed_tenant_types


# -------------------------PROVEEDOR--------------------------


@admin.register(Giro)
class GiroAdmin(SharedModelAdminBase):
    pass


@admin.register(Rubro)
class RubroAdmin(SharedModelAdminBase):
    pass


@admin.register(Proveedor)
class ProveedorAdmin(SharedModelAdminBase):
    list_display = (
        "id_proveedor",
        "run_proveedor",
        "nombre_proveedor",
        "telefono_proveedor",
    )
