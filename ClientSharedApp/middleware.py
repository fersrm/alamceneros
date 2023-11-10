from django.http import HttpResponseRedirect
from django_tenants.utils import get_public_schema_name


class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar si el esquema es public
        current_tenant_name = request.tenant.schema_name
        public_schema_name = get_public_schema_name()
        if current_tenant_name == public_schema_name:
            # Verificar si la solicitud no está en /admin/
            if not (request.path.startswith("/admin/")):
                return HttpResponseRedirect("/admin/")

        return self.get_response(request)
