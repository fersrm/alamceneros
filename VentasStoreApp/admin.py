from django.contrib import admin
from VentasStoreApp.models import Boletas, Ventas

# Register your models here.

# ------------------FACTURAS-BOLETAS---------------


def generate_voucher(model, user_field_name):
  class CustomAdmin(admin.ModelAdmin):
    # readonly_fields = ('fecha_emision',)

    # def vendedor(self, obj):
    #   return getattr(obj, user_field_name)
    # vendedor.short_description = 'Vendedor'
    id_field = 'id_boleta' if hasattr(model, 'id_boleta') else 'id_factura'
    list_display = (
        id_field,
        'total_factura' if hasattr(
            model,
            'total_factura') else 'total_boleta')
  return CustomAdmin


admin.site.register(Boletas, generate_voucher(Boletas, 'usuario_FK'))


# ------------------Ventas--------------


class VentasAdmin(admin.ModelAdmin):
  list_display = ('id_venta', 'fecha_emision', 'usuario_FK')


admin.site.register(Ventas, VentasAdmin)
