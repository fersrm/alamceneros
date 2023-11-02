from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from VentasStoreApp.models import Boletas, DetalleBoletas
from ProductosStoreApp.models import Producto
# Para trabajar con clases
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from django.urls import reverse_lazy

# imporat funciones
from utils.helpers import top_productos, total_dia, total_ventas

# Create your views here.


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class HomeView(TemplateView):
  template_name = 'home.html'
  success_url = reverse_lazy('Home')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    # Obtiene el valor de 'periodo' del parámetro GET
    periodo = self.request.GET.get('periodo', 'dia')
    if periodo not in ['dia', 'semana', 'mes']:
      periodo = 'dia'
    ventas_diarias = total_ventas(Boletas, periodo)
    context['ventas_diarias'] = ventas_diarias
    context['mi_fecha'] = timezone.localtime(timezone.now()).date()

    # Boletas ---------------------------------
    boletas_data = total_dia(
        Boletas,
        'cantidad_boletas',
        'total_boleta')  # total_boleta es el nombre del campo en la BBDD
    context.update(boletas_data)
    # Top Productos Ventas ---------------------
    campos_producto = (
        'codigo_producto',
        'descripcion_producto',
        'categoria_FK__nombre_categoria',
        'stock',
        'precio_venta',
    )
    top_mas_vendidos, top_menos_vendidos = top_productos(
        Producto, DetalleBoletas, campos_producto)
    context['top_mas_vendidos'] = top_mas_vendidos
    context['top_menos_vendidos'] = top_menos_vendidos
    return context


# --------------------SALIR---------------------


class SalirView(LogoutView):
  next_page = '/'

  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)
