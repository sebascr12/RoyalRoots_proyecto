from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="index.html"), name='home'),  # Página principal
    path('empleados/', include('empleados.urls')),  # Módulo empleados
    path('direcciones/', include('direcciones.urls')),  # Módulo direcciones
    path('clientes/', include('clientes.urls')),
    path('producto/', include('producto.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('reservas/', include('reservas.urls')),
    path('facturacion/', include('facturacion.urls')),
    path('usuarios/', include('usuarios.urls')),

]
