from django.contrib import admin
from DatosEmpresaStoreApp.models import DatosEmpresa

# Register your models here.

# ------------DATOS-EMPRESA-------


class EmpresaAdmin(admin.ModelAdmin):
  list_display = ('id_datos_empresa', 'nombre_empresa')


admin.site.register(DatosEmpresa, EmpresaAdmin)
