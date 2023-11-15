from django.urls import path
from FacturasStoreApp import views


urlpatterns = [
    path("", views.VentasFacturasListView.as_view(), name="Facturas"),
    path("informe_factura/", views.BoletaListView.as_view(), name="Informe_facturas"),
]
