# from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from utils.custom_middleware import cargo_check
from django.shortcuts import get_object_or_404
from django.contrib import messages
from decimal import Decimal

# Modelos y formularios
from .models import Boletas, Ventas, DetalleBoletas
from .forms import VentasForm
from django.db.models import F, Case, When, Value, IntegerField

# Para trabajar con clases
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

# imporat funciones
from utils.helpers import buscar_fecha_rango, buscar_venta, buscar_fecha

from ProductosStoreApp.models import Producto
from FacturasStoreApp.models import Facturas

# -------------------INFORMES----------


@method_decorator(login_required(login_url="/login/"), name="dispatch")
@method_decorator(cargo_check, name="dispatch")
class InformesListView(ListView):
    model = Boletas
    template_name = "Informes.html"

    def get_queryset(self):
        fecha1 = self.request.GET.get("buscarFecha1")
        fecha2 = self.request.GET.get("buscarFecha2")

        # Validar por Typo de esquema
        tenant_type = self.request.tenant.type
        allowed_tenant_types = ["type2"]

        if tenant_type in allowed_tenant_types:
            queryset = buscar_fecha_rango(self.model, fecha1, fecha2, Facturas)
        else:
            queryset = buscar_fecha_rango(self.model, fecha1, fecha2)
        return queryset


# --------------INFORME PDF BOLETAS ---------------------


@method_decorator(login_required(login_url="/login/"), name="dispatch")
@method_decorator(cargo_check, name="dispatch")
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


# -----------------------Ventas Boletas--------------------


@method_decorator(login_required(login_url="/login/"), name="dispatch")
class VentasBoletaListView(CreateView, ListView):
    model = Ventas
    form_class = VentasForm
    template_name = "ventas.html"

    def form_valid(self, form):
        usuario_logeado = self.request.user
        venta = form.save(commit=False)
        venta.usuario_FK = usuario_logeado
        venta.save()

        # Obtener Carrito ------------------------------
        carrito = form.cleaned_data["carrito"]

        carrito = carrito_json(carrito)
        # --------------------------------------------

        total_boleta = calcular_total_ventas(carrito)

        boleta = Boletas(total_boleta=total_boleta, venta_FK=venta)

        boleta.save()

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

            detalle_boleta = DetalleBoletas(
                cantidad=cantidad, total=total, producto_FK=producto, boleta_FK=boleta
            )
            detalle_boleta.save()

            if medida == 1:
                producto.stock -= Decimal(cantidad)
            else:
                cantidad = Decimal(cantidad) / Decimal(1000)
                producto.stock -= cantidad

            producto.save()

        success_message = "Venta Generada con Éxito"
        messages.success(self.request, success_message, extra_tags="success-venta")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error en el formulario")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")
        return HttpResponseRedirect("/ventas/")

    def get_success_url(self):
        return reverse_lazy("Ventas")

    def get_queryset(self):
        busqueda = self.request.GET.get("buscar")
        queryset = Producto.objects.filter(codigo_producto__exact=busqueda)

        if queryset and busqueda:
            descuento_promocion = Case(
                When(promociones__activo=True, then=F("promociones__descuento")),
                default=Value(0),
                output_field=IntegerField(),
            )

            queryset = queryset.annotate(descuento=descuento_promocion)

            if queryset.count() == 1:
                queryset = queryset.annotate(descuento=descuento_promocion)

            elif queryset.count() > 1:
                filtra_queryset = queryset.annotate(
                    descuento=descuento_promocion
                ).filter(descuento__gt=0)

                if filtra_queryset:
                    queryset = filtra_queryset

        elif not queryset and busqueda:
            messages.error(self.request, f"No existe {busqueda}")

        queryset = queryset.first()
        return queryset


def calcular_total_ventas(carrito):
    descuento_total = 0
    total = 0
    for item in carrito:
        descuento = item["descuento"]
        total_producto = 0
        if item["medida"] == 1:
            total_producto += item["cantidad"] * item["precio"]
        else:
            cantidad_kilos = item["cantidad"] / 1000
            costo_total = cantidad_kilos * item["precio"]
            costo_total = round(costo_total)
            total_producto += costo_total

        total += total_producto

        monto_descuento = (descuento / 100) * total_producto
        descuento_total = round(monto_descuento)

    total = total - descuento_total
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
