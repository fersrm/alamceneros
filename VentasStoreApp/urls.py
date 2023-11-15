from django.urls import path
from VentasStoreApp import views


urlpatterns = [
    path("", views.VentasBoletaListView.as_view(), name="Ventas"),
    path("informe_boletas/", views.BoletaListView.as_view(), name="Boletas"),
    path("informes/", views.InformesListView.as_view(), name="Informes"),
]
