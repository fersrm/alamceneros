from django.urls import path
from PromocionesStoreApp import views

urlpatterns = [
    path("", views.AgregarPromocionesView.as_view(), name="Promociones"),
    path(
        "obtener_productos_por_categoria/",
        views.obtener_productos_por_categoria,
        name="obtener_productos_por_categoria",
    ),
]
