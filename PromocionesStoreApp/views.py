# Librerías de Django
from django.http import JsonResponse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from utils.custom_middleware import cargo_check
from django.contrib import messages
from django.db.models import Q

# Modelos y formularios
from .forms import PromocionesForm
from .models import Promociones, Producto

# Para trabajar con clases

from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy

# Create your views here.


@method_decorator(login_required(login_url="/login/"), name="dispatch")
@method_decorator(cargo_check, name="dispatch")
class AgregarPromocionesView(CreateView, ListView):
    model = Promociones
    form_class = PromocionesForm
    template_name = "promociones.html"

    def form_valid(self, form):
        form.save()
        success_message = "Promocion agregada correctamente"
        messages.success(self.request, success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error en el formulario")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")
        return HttpResponseRedirect("/promociones/")

    def get_success_url(self):
        return reverse_lazy("Promociones")

    def get_queryset(self):
        busqueda = self.request.GET.get("buscar", "").upper()
        queryset = self.model.objects.all()

        if busqueda == "ACTIVO":
            queryset = queryset.filter(activo=True)
        elif busqueda == "DESACTIVADO":
            queryset = queryset.filter(activo=False)
        elif busqueda:
            queryset = queryset.filter(
                Q(producto_FK__descripcion_producto__icontains=busqueda)
                | Q(producto_FK__codigo_producto__exact=busqueda)
            )

            if not queryset:
                messages.error(self.request, f"NO HAY PROMOCIÓN {busqueda}")

        return queryset.order_by("-id_promocion")


@cargo_check
def obtener_productos_por_categoria(request):
    categoria_id = request.GET.get("categoria_id")

    if not categoria_id:
        productos = Producto.objects.all().values("pk", "descripcion_producto")
    else:
        productos = Producto.objects.filter(categoria_FK_id=categoria_id).values(
            "pk", "descripcion_producto"
        )

    productos_list = list(productos)

    return JsonResponse({"productos": productos_list}, safe=False)
