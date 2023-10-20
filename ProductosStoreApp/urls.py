from django.urls import path
from ProductosStoreApp import views

urlpatterns = [
    # ---------CRUD PRODUCTOS----------------------
    path('', views.ProductoListView.as_view(), name='Tienda'),
    path(
        'agregar/',
        views.AgregarProductoView.as_view(),
        name='agregar_prodcuto'),
    path(
        'editar/<int:pk>/',
        views.EditarProductoView.as_view(),
        name='editar_producto'),
    path(
        'borrar/<int:pk>/',
        views.EliminarProductoView.as_view(),
        name='eliminar_producto'),
    # -------------AÑADIDO PRODUCTOS----------------
    path(
        'plus/<int:pk>/',
        views.PlusProductoView.as_view(),
        name='añadir_producto'),
    # ---------------NOTIFICASIONES------------------
    path('tabla_stock/', views.tabla_stock, name='tabla_stock'),
]
