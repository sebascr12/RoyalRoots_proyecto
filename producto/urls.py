from django.urls import path
from . import views

urlpatterns = [
    path('producto/listar/', views.listar_productos_view, name='listar_productos'),
    path('producto/insertar/', views.insertar_producto_view, name='insertar_producto'),
    path('producto/actualizar/<int:id_producto>/', views.actualizar_producto_view, name='actualizar_producto'),
    path('producto/inactivar/<int:id_producto>/', views.inactivar_producto_view, name='inactivar_producto'),

    path('inventario/listar/', views.listar_inventario_view, name='listar_inventario'),
    path('inventario/insertar/', views.insertar_inventario_view, name='insertar_inventario'),
    path('inventario/actualizar/<int:id_inventario>/', views.actualizar_inventario_view, name='actualizar_inventario'),
    path('inventario/inactivar/<int:id_inventario>/', views.inactivar_inventario_view, name='inactivar_inventario'),


    path('proveedor/listar/', views.listar_proveedores_view, name='listar_proveedores'),
    path('proveedor/insertar/', views.insertar_proveedor_view, name='insertar_proveedor'),
    path('proveedor/actualizar/<int:id_proveedor>/', views.actualizar_proveedor_view, name='actualizar_proveedor'),
    path('proveedor/inactivar/<int:id_proveedor>/', views.inactivar_proveedor_view, name='inactivar_proveedor'),

    path('ordenes/listar/', views.listar_ordenes_view, name='listar_ordenes'),
    path('ordenes/insertar/', views.insertar_orden_view, name='insertar_orden'),
    path('ordenes/actualizar/<int:id_orden>/', views.actualizar_orden_view, name='actualizar_orden'),
    path('ordenes/inactivar/<int:id_orden>/', views.inactivar_orden_view, name='inactivar_orden'),

]
