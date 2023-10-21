from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('SistemaStoreApp.urls')),
    path('tienda/', include('ProductosStoreApp.urls')),
    path('usuarios/', include('UsuariosStoreApp.urls')),
    path('setting/', include('DatosEmpresaStoreApp.urls')),
    path('ventas/', include('VentasStoreApp.urls')),
    path('clientes/', include('ClientesStoreApp.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
