from django.urls import path
from . import views

urlpatterns = [
    path('listar/', views.listar_servicios_view, name='listar_servicios'),
    path('insertar/', views.insertar_servicio_view, name='insertar_servicio'),
    path('actualizar/<str:nombre_actual>/', views.actualizar_servicio_view, name='actualizar_servicio'),
    path('inactivar/<str:nombre_servicio>/', views.inactivar_servicio_view, name='inactivar_servicio'),

    #beneficios
    path('beneficios/listar/', views.listar_beneficios_view, name='listar_beneficios'),
    path('beneficios/insertar/', views.insertar_beneficio_view, name='insertar_beneficio'),
    path('beneficios/actualizar/<str:detalle_actual>/', views.actualizar_beneficio_view, name='actualizar_beneficio'),
    path('beneficios/inactivar/<str:detalle_beneficio>/', views.inactivar_beneficio_view, name='inactivar_beneficio'),

    ##clientes
      path('clientes/listar/', views.listar_clientes_view, name='listar_clientes'),
    path('clientes/insertar/', views.insertar_cliente_view, name='insertar_cliente'),
    path('clientes/actualizar/<int:id_cliente>/', views.actualizar_cliente_view, name='actualizar_cliente'),
    path('clientes/inactivar/<int:id_cliente>/', views.inactivar_cliente_view, name='inactivar_cliente'),

]