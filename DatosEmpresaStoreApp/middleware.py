from .models import DatosEmpresa
from django_tenants.utils import get_public_schema_name


class DatosEmpresaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.tenant.schema_name != get_public_schema_name():
            datos_empresa = DatosEmpresa.objects.filter(id_datos_empresa=1).first()

            request.datos_empresa = datos_empresa

            response = self.get_response(request)
            return response
        else:
            return self.get_response(request)
