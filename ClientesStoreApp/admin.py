from django.contrib import admin
from .models import Cliente, Region, Comuna

# Register your models here.

admin.site.register(Comuna)
admin.site.register(Region)

# -------------------------CLIENTE--------------------------


class ClienteAdmin(admin.ModelAdmin):
  def comuna(self, obj):
    return getattr(obj, 'comuna_FK')
  comuna.short_description = 'Comuna'
  list_display = (
      'id_cliente',
      'run_cliente',
      'nombre_cliente',
      'apellido_cliente',
      'comuna')


admin.site.register(Cliente, ClienteAdmin)
