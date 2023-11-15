# from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.contrib import messages
from decimal import Decimal

# Modelos y formularios
from .models import Facturas, Ventas, DetalleFacturas, Cliente
from .forms import VentasFacturasForm

# Para trabajar con clases
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy


from ProductosStoreApp.models import Producto

# imporat funciones
from utils.helpers import buscar_venta, buscar_fecha


# -----------------------Ventas Factura--------------------


@method_decorator(login_required(login_url="/login/"), name="dispatch")
class VentasFacturasListView(CreateView, ListView):
    model = Ventas
    form_class = VentasFacturasForm
    template_name = "facturas.html"

    def form_valid(self, form):
        usuario_logeado = self.request.user
        venta = form.save(commit=False)
        venta.usuario_FK = usuario_logeado
        venta.save()

        # Obtener Carrito ---------------------------
        carrito = form.cleaned_data["carrito"]

        carrito = carrito_json(carrito)
        # --------------------------------------------

        # Obtener Cliente ---------------------------
        cliente = form.cleaned_data["cliente_id"]
        # Convertir el valor a una instancia de Cliente
        cliente_instance = get_object_or_404(Cliente, pk=cliente)
        # --------------------------------------------

        total_factura = calcular_total_ventas(carrito)

        factura = Facturas(
            total_factura=total_factura, venta_FK=venta, cliente_fk=cliente_instance
        )

        factura.save()

        for item in carrito:
            producto = get_object_or_404(Producto, id_producto=item["id"])
            cantidad = item["cantidad"]
            precio = item["precio"]
            medida = item["medida"]

            if medida == 1:
                total = cantidad * precio
            else:
                cantidad_kilos = cantidad / 1000
                costo_total = cantidad_kilos * precio
                costo_total = round(costo_total)
                total = costo_total

            detalle_factura = DetalleFacturas(
                cantidad=cantidad, total=total, producto_FK=producto, factura_FK=factura
            )
            detalle_factura.save()

            if medida == 1:
                producto.stock -= Decimal(cantidad)
            else:
                cantidad = Decimal(cantidad) / Decimal(1000)
                producto.stock -= cantidad

            producto.save()

        success_message = "Venta Generada con Éxito"
        messages.success(self.request, success_message, extra_tags="success-factura")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error en el formulario")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return HttpResponseRedirect("/facturas/")

    def get_success_url(self):
        return reverse_lazy("Facturas")

    def get_queryset(self):
        busqueda = self.request.GET.get("buscar")
        busqueda_cliente = self.request.GET.get("buscar_cliente")

        queryset = Producto.objects.filter(codigo_producto__exact=busqueda)
        queryset_cliente = Cliente.objects.filter(run_cliente__exact=busqueda_cliente)

        if not queryset and busqueda:
            messages.error(self.request, f"No existe {busqueda}")
        elif not queryset_cliente and busqueda_cliente:
            messages.error(self.request, f"No existe {busqueda_cliente}")
        else:
            if queryset:
                return queryset
            elif queryset_cliente:
                return queryset_cliente

        return []


def calcular_total_ventas(carrito):
    total = 0
    for item in carrito:
        if item["medida"] == 1:
            total += item["cantidad"] * item["precio"]
        else:
            cantidad_kilos = item["cantidad"] / 1000
            costo_total = cantidad_kilos * item["precio"]
            costo_total = round(costo_total)
            total = costo_total

    return total


def carrito_json(carrito_str):
    import json

    try:
        carrito_list = json.loads(carrito_str)

        if isinstance(carrito_list, list):
            return carrito_list
        else:
            return []
    except json.JSONDecodeError:
        return []


# --------------INFORME PDF BOLETAS ---------------------


@method_decorator(login_required(login_url="/login/"), name="dispatch")
class BoletaListView(ListView):
    model = Facturas
    template_name = "informeFactura.html"

    def get_queryset(self):
        busqueda = self.request.GET.get("buscar")
        busquedaF = self.request.GET.get("buscarFecha")
        campos_busqueda = ["id_factura", "total_factura"]
        if busquedaF:
            queryset = buscar_fecha(self.model, busquedaF)
        else:
            queryset = buscar_venta(self.model, campos_busqueda, busqueda)
        queryset = queryset.order_by("-id_factura")
        return queryset