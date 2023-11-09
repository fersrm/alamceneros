from django.urls import path
from VentasStoreApp import views


urlpatterns = [

    path('', views.PagosListView.as_view(), name='Ventas'),
    path('informe_Boletas/', views.BoletaListView.as_view(), name='Boletas'),
    path('informes/', views.InformesListView.as_view(), name='Informes'),

]
