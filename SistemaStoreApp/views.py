from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from VentasStoreApp.models import Boletas, DetalleBoletas
from ComprasStoreApp.models import Compras
from ProductosStoreApp.models import Producto
from FacturasStoreApp.models import Facturas, DetalleFacturas

# Para trabajar con clases
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from django.urls import reverse_lazy

# imporat funciones
from utils.helpers import top_productos, total_dia, total_ventas

# Create your views here.


@method_decorator(login_required(login_url="/login/"), name="dispatch")
class HomeView(TemplateView):
    template_name = "home.html"
    success_url = reverse_lazy("Home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtiene el valor de 'periodo' del parámetro GET
        periodo = self.request.GET.get("periodo", "dia")
        if periodo not in ["dia", "semana", "mes"]:
            periodo = "dia"

        # Validar por Typo de esquema
        tenant_type = self.request.tenant.type
        allowed_tenant_types = ["type2"]

        if tenant_type in allowed_tenant_types:
            ventas_diarias, compras_totales = total_ventas(
                Boletas, Compras, periodo, Facturas
            )
        else:
            ventas_diarias, compras_totales = total_ventas(Boletas, Compras, periodo)

        context["ventas_diarias"] = ventas_diarias
        context["compras_totales"] = compras_totales
        context["mi_fecha"] = timezone.localtime(timezone.now()).date()

        # Boletas ---------------------------------
        boletas_data = total_dia(Boletas, "cantidad_boletas", "total_boleta")
        context.update(boletas_data)
        # Top Productos Ventas ---------------------
        campos_producto = (
            "codigo_producto",
            "descripcion_producto",
            "categoria_FK__nombre_categoria",
            "stock",
            "precio_venta",
        )
        if tenant_type in allowed_tenant_types:
            top_mas_vendidos, top_menos_vendidos = top_productos(
                Producto, DetalleBoletas, campos_producto, DetalleFacturas
            )
            # Facturas ---------------------------------
            factura_data = total_dia(Facturas, "cantidad_factura", "total_factura")
            context.update(factura_data)
        else:
            top_mas_vendidos, top_menos_vendidos = top_productos(
                Producto, DetalleBoletas, campos_producto
            )
        context["top_mas_vendidos"] = top_mas_vendidos
        context["top_menos_vendidos"] = top_menos_vendidos
        return context


# --------------------SALIR---------------------


class SalirView(LogoutView):
    next_page = "/"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
