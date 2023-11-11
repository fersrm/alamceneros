# from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.contrib import messages

# Modelos y formularios
from .models import Boletas, Ventas, DetalleBoletas
from .forms import VentasForm

# Para trabajar con clases
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

# imporat funciones
from utils.helpers import buscar_fecha_rango, buscar_venta, buscar_fecha

from ProductosStoreApp.models import Producto

# -------------------INFORMES----------


@method_decorator(login_required(login_url="/login/"), name="dispatch")
class InformesListView(ListView):
    model = Ventas
    template_name = "Informes.html"

    def get_queryset(self):
        fecha1 = self.request.GET.get("buscarFechaRango1")
        fecha2 = self.request.GET.get("buscarFechaRango2")
        periodo = self.request.GET.get("periodo", "mensual")

        return buscar_fecha_rango(self.model, fecha1, fecha2, periodo)


# --------------INFORME PDF BOLETAS ---------------------


@method_decorator(login_required(login_url="/login/"), name="dispatch")
class BoletaListView(ListView):
    model = Boletas
    template_name = "informeBoleta.html"

    def get_queryset(self):
        busqueda = self.request.GET.get("buscar")
        busquedaF = self.request.GET.get("buscarFecha")
        campos_busqueda = ["id_boleta", "total_boleta"]
        if busquedaF:
            queryset = buscar_fecha(self.model, busquedaF)
        else:
            queryset = buscar_venta(self.model, campos_busqueda, busqueda)
        queryset = queryset.order_by("-id_boleta")
        return queryset


# -----------------------PAGOS--------------------


@method_decorator(login_required(login_url="/login/"), name="dispatch")
class PagosListView(CreateView, ListView):
    model = Ventas
    form_class = VentasForm
    template_name = "ventas.html"

    def form_valid(self, form):
        usuario_logeado = self.request.user
        venta = form.save(commit=False)
        venta.usuario_FK = usuario_logeado
        venta.save()

        # Obtener Carrito ------------------------------
        carrito = form.cleaned_data['carrito']

        carrito = carrito_json(carrito)
        print(carrito)
        # --------------------------------------------

        total_boleta = calcular_total_ventas(carrito)

        boleta = Boletas(total_boleta=total_boleta, venta_FK=venta)

        boleta.save()

        for item in carrito:
            producto = get_object_or_404(Producto, id_producto=item['id'])
            cantidad = item['cantidad']
            precio = item['precio']

            total = cantidad * precio

            detalle_boleta = DetalleBoletas(
                cantidad=cantidad,
                total=total,
                producto_FK=producto,
                boleta_FK=boleta
            )
            detalle_boleta.save()

            producto.stock -= cantidad
            producto.save()

        success_message = "Venta Generada con Existo"
        messages.success(self.request, success_message,
                         extra_tags="success-venta")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error en el formulario")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return HttpResponseRedirect("/ventas/")

    def get_success_url(self):
        return reverse_lazy("Ventas")

    def get_queryset(self):
        busqueda = self.request.GET.get("buscar")
        queryset = Producto.objects.filter(codigo_producto__exact=busqueda)
        if not queryset and busqueda:
            messages.error(self.request, f"No Existe {busqueda}")
        return queryset


def calcular_total_ventas(carrito):
    total = 0
    for item in carrito:
        total += item['cantidad'] * item['precio']
    return total


def carrito_json(carrito_str):
    import json

    try:

        carrito_list = json.loads(carrito_str)

        if isinstance(carrito_list, list):
            print(carrito_list)
            return carrito_list
        else:

            return []
    except json.JSONDecodeError:
        return []
