from django.conf import settings
from django.shortcuts import redirect
from django_tenants.utils import get_public_schema_name


class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        public_schema_name = get_public_schema_name()
        current_tenant_name = request.tenant.schema_name

        if response.status_code == 404 and current_tenant_name != public_schema_name:
            if request.user.is_authenticated:
                return redirect("Home")
            else:
                return redirect("login")
        else:
            return response


class TenantAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_tenant_type = request.tenant.type
        # print(current_tenant_type)
        tenant_types = settings.TENANT_TYPES

        enabled_apps = tenant_types.get(current_tenant_type, {}).get("APPS", [])

        request.enabled_apps = enabled_apps
        response = self.get_response(request)
        return response


def cargo_check(function):
    def wrap(request, *args, **kwargs):
        if request.tenant.schema_name != get_public_schema_name():
            if request.user.is_authenticated and request.user.cargo_FK.id_cargo == 3:
                return redirect("Home")

        return function(request, *args, **kwargs)

    return wrap
