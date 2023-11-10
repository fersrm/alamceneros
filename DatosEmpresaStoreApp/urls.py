from django.urls import path
from DatosEmpresaStoreApp import views


urlpatterns = [
    path("", views.editar_datos_empresa, name="Setting"),
]
