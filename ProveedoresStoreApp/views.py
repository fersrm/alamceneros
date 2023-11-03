# Librerías de Django
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect
# Modelos y formularios
from .forms import ProveedorAgregarForm, ProveedorEditarForm
from .models import Proveedor

# Para trabajar con clases

from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

# imporat funciones
from utils.helpers import buscar_campos
# Create your views here.

# ---------------CRUD Proveedores------------


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ProveedorListView(ListView):
  model = Proveedor
  template_name = 'proveedor.html'
  paginate_by = 7

  def get_queryset(self):
    busqueda = self.request.GET.get('buscar')
    campos_busqueda = [
        'run_proveedor',
        'nombre_proveedor',
        'correo_proveedor'
    ]
    queryset = buscar_campos(
        self.model, campos_busqueda, busqueda)
    queryset = queryset.order_by('-id_proveedor')
    return queryset

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    paginator = Paginator(context['object_list'], self.paginate_by)
    page = self.request.GET.get('page')
    context['object_list'] = paginator.get_page(page)
    return context

# -------------------------------------------------


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class AgregarProveedorView(CreateView):
  model = Proveedor
  form_class = ProveedorAgregarForm
  template_name = 'modal/AddProveedor.html'

  def form_valid(self, form):
    form.save()
    messages.success(self.request, "Proveedor agregado correctamente")
    return super().form_valid(form)

  def form_invalid(self, form):
    messages.error(self.request, 'Error en el formulario')
    for field, errors in form.errors.items():
      for error in errors:
        messages.error(self.request, f"{field}: {error}")
    return HttpResponseRedirect('/proveedores/')

  def get_success_url(self):
    return reverse_lazy('Proveedores')
# -------------------------------------------------


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class EditarProveedorView(UpdateView):
  model = Proveedor
  form_class = ProveedorEditarForm
  template_name = 'modal/EditProveedor.html'

  def form_valid(self, form):
    form.clean()
    form.save()
    messages.success(self.request, "Proveedor Editado correctamente")
    return super().form_valid(form)

  def form_invalid(self, form):
    messages.error(self.request, 'Error en el formulario')
    for field, errors in form.errors.items():
      for error in errors:
        messages.error(self.request, f"{field}: {error}")
    return HttpResponseRedirect('/proveedores/')

  def get_success_url(self):
    return reverse_lazy('Proveedores')
# --------------------------------------------------


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class EliminarProveedorView(DeleteView):
  model = Proveedor
  success_url = reverse_lazy('Proveedores')

  def get(self, request, *args, **kwargs):
    self.object = self.get_object()

    messages.success(self.request, "Proveedor eliminado correctamente")
    self.object.delete()
    return redirect(self.get_success_url())
