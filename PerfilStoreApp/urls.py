from django.urls import path
from PerfilStoreApp import views


urlpatterns = [
    path('', views.editar_perfil, name='Perfil'),
]
