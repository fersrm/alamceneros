from .models import Producto
from django.db.models import Q
from django_tenants.utils import get_public_schema_name


class ProductosStockMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.tenant.schema_name != get_public_schema_name():
            # Obtener productos con stock bajo
            productos_con_stock_bajo = Producto.objects.filter(
                Q(stock__lt=10) & Q(tipo_medida=1)
            )

            # Agregar el contexto global
            request.productos_con_stock_bajo = productos_con_stock_bajo

            response = self.get_response(request)
            return response

        else:
            return self.get_response(request)
