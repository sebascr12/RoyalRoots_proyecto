from django.urls import path
from . import views

urlpatterns = [
    path('metodo_pago/listar/', views.listar_metodos_pago_view, name='listar_metodos_pago'),
    path('metodo_pago/insertar/', views.insertar_metodo_pago_view, name='insertar_metodo_pago'),
    path('metodo_pago/actualizar/<int:id_metodo>/', views.actualizar_metodo_pago_view, name='actualizar_metodo_pago'),
    path('metodo_pago/inactivar/<int:id_metodo>/', views.inactivar_metodo_pago_view, name='inactivar_metodo_pago'),


    path('historial_pagos/listar/', views.listar_historial_pagos_view, name='listar_historial_pagos'),
    path('historial_pagos/insertar/', views.insertar_historial_pago_view, name='insertar_historial_pago'),
    path('historial_pagos/actualizar/<int:id_pago>/', views.actualizar_historial_pago_view, name='actualizar_historial_pago'),
    path('historial_pagos/inactivar/<int:id_pago>/', views.inactivar_historial_pago_view, name='inactivar_historial_pago'),

    path('facturas/listar/', views.listar_facturas_view, name='listar_facturas'),
    path('facturas/insertar/', views.insertar_factura_view, name='insertar_factura'),
    path('facturas/actualizar/<int:id_factura>/', views.actualizar_factura_view, name='actualizar_factura'),
    path('facturas/inactivar/<int:id_factura>/', views.inactivar_factura_view, name='inactivar_factura'),

    path('detalle_facturas/listar/', views.listar_detalles_factura_view, name='listar_detalles_factura'),
    path('detalle_facturas/insertar/', views.insertar_detalle_factura_view, name='insertar_detalle_factura'),
    path('detalle_facturas/actualizar/<int:id_detalle>/', views.actualizar_detalle_factura_view, name='actualizar_detalle_factura'),
    path('detalle_facturas/inactivar/<int:id_detalle>/', views.inactivar_detalle_factura_view, name='inactivar_detalle_factura'),


]
