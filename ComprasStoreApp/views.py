# Librerías de Django
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from utils.custom_middleware import cargo_check
from django.contrib import messages

# Modelos y formularios
from .forms import ComprasAgregarForm
from .models import Compras

# modelos de productos
from ProductosStoreApp.models import Producto
from ProductosStoreApp.forms import PlusProductoForm

# Para trabajar con clases

from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy

# Create your views here.


@method_decorator(login_required(login_url="/login/"), name="dispatch")
@method_decorator(cargo_check, name="dispatch")
class AgregarCompraView(CreateView, ListView):
    model = Compras
    form_class = ComprasAgregarForm
    template_name = "compras.html"

    def form_valid(self, form):
        form.save()
        success_message = "Compra agregada correctamente"
        messages.success(self.request, success_message, extra_tags="success-alert")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error en el formulario")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return HttpResponseRedirect("/compras/")

    def get_success_url(self):
        return reverse_lazy("Compras")

    def get_queryset(self):
        busqueda = self.request.GET.get("buscar")
        queryset = Producto.objects.filter(codigo_producto__exact=busqueda)

        if not queryset and busqueda:
            messages.error(self.request, f"No existe {busqueda}")
        return queryset


@method_decorator(login_required(login_url="/login/"), name="dispatch")
@method_decorator(cargo_check, name="dispatch")
class CompraProductoView(UpdateView):
    model = Producto
    form_class = PlusProductoForm
    template_name = "modal/CompraProduc.html"

    def form_valid(self, form):
        producto = form.instance
        stock_increment = form.cleaned_data.get("stock_increment")
        if stock_increment is not None:
            producto.stock += stock_increment
        form.save()
        success_message = "Producto añadido correctamente"
        messages.success(self.request, success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error en el formulario")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return HttpResponseRedirect("/compras/")

    def get_success_url(self):
        return reverse_lazy("Compras")
