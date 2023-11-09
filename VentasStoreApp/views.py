# from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Modelos y formularios
from .models import Boletas, Ventas
# Para trabajar con clases
from django.views.generic import ListView
# imporat funciones
from utils.helpers import buscar_fecha_rango, buscar_venta, buscar_fecha

from ProductosStoreApp.models import Producto
# -------------------INFORMES----------


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class InformesListView(ListView):
    model = Ventas
    template_name = 'Informes.html'

    def get_queryset(self):
        fecha1 = self.request.GET.get('buscarFechaRango1')
        fecha2 = self.request.GET.get('buscarFechaRango2')
        periodo = self.request.GET.get('periodo', 'mensual')

        return buscar_fecha_rango(
            self.model, fecha1, fecha2, periodo)


# --------------INFORME PDF BOLETAS ---------------------

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class BoletaListView(ListView):
    model = Boletas
    template_name = 'informeBoleta.html'

    def get_queryset(self):
        busqueda = self.request.GET.get('buscar')
        busquedaF = self.request.GET.get('buscarFecha')
        campos_busqueda = [
            'id_boleta',
            'total_boleta']
        if busquedaF:
            queryset = buscar_fecha(self.model, busquedaF)
        else:
            queryset = buscar_venta(self.model, campos_busqueda, busqueda)
        queryset = queryset.order_by('-id_boleta')
        return queryset


# -----------------------PAGOS--------------------

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class PagosListView(ListView):
    model = Ventas
    template_name = 'ventas.html'

    def get_queryset(self):
        busqueda = self.request.GET.get('buscar')
        queryset = Producto.objects.filter(codigo_producto__exact=busqueda)
        return queryset
