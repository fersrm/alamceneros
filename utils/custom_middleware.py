from django.conf import settings
# from tenant_schemas.utils import get_public_schema_name
from django.shortcuts import redirect, render


class RedirectMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    response = self.get_response(request)

    if response.status_code == 404:
      if request.user.is_authenticated:
        return redirect('Home')
      else:
        return redirect('login')

    return response


class TenantAccessMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    current_tenant_type = request.tenant.choices

    tenant_types = settings.TENANT_TYPES

    enabled_apps = tenant_types.get(current_tenant_type, {}).get("APPS", [])

    request.enabled_apps = enabled_apps
    response = self.get_response(request)
    return response


class TenantAccessUrlMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    # obtiene el  esquema #
    current_tenant_type = request.tenant.choices

    tenant_types = settings.TENANT_TYPES
    enabled_apps = tenant_types.get(current_tenant_type, {}).get("APPS", [])

    # Obtiene la URL solicitada por el usuario
    requested_url = request.path

    url_to_app_mapping = {
        "/clientes/": {"app": "ClientesStoreApp", },
        # Add aqui mas patrones de URL
    }

    app = None
    for url_pattern, app_config in url_to_app_mapping.items():

      if requested_url.startswith(url_pattern):
        app = app_config["app"]

        if app is not None and app not in enabled_apps:
          return render(request, "forbidden_template.html", status=403)

    return self.get_response(request)
