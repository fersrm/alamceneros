# from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
# Modelos y formularios
from .models import Boletas, Ventas
# Para trabajar con clases
from django.views.generic import ListView
# imporat funciones
from utils.helpers import buscar_fecha_rango, buscar_campos

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

  # -----------------------PAGOS----------


# ------------------INFORMES-PDF------------------

# -----------------------BOLETAS-------------------


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class BoletaListView(ListView):
  model = Boletas
  template_name = 'informeBoleta.html'
  paginate_by = 10

  def get_queryset(self):
    busqueda = self.request.GET.get('buscar')
    busquedaF = self.request.GET.get('buscarFecha')
    campos_busqueda = [
        'id_boleta',
        'total_boleta']
    return buscar_campos(
        self.model, campos_busqueda, busqueda, busquedaF)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    paginator = Paginator(context['object_list'], self.paginate_by)
    page = self.request.GET.get('page')
    context['object_list'] = paginator.get_page(page)
    return context


# -----------------------PAGOS--------------------

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class PagosListView(ListView):
  model = Ventas
  template_name = 'pagos.html'
