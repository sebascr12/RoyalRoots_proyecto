from django.urls import path
from . import views

urlpatterns = [
    path('provincias/listar/', views.listar_provincias_view, name='listar_provincias'),
    path('provincias/insertar/', views.insertar_provincia_view, name='insertar_provincia'),
    path('provincias/actualizar/<str:nombre_actual>/', views.actualizar_provincia_view, name='actualizar_provincia'),
    path('provincias/inactivar/<str:nombre_provincia>/', views.inactivar_provincia_view, name='inactivar_provincia'),

    ##canton
    path('cantones/listar/', views.listar_cantones_view, name='listar_cantones'),
    path('cantones/insertar/', views.insertar_canton_view, name='insertar_canton'),
    path('cantones/actualizar/<str:nombre_actual>/', views.actualizar_canton_view, name='actualizar_canton'),
    path('cantones/inactivar/', views.inactivar_canton_view, name='inactivar_canton'),

    ##distrito
    path('distritos/listar/', views.listar_distritos_view, name='listar_distritos'),
    path('distritos/insertar/', views.insertar_distrito_view, name='insertar_distrito'),
    path('distritos/actualizar/<str:nombre_actual>/', views.actualizar_distrito_view, name='actualizar_distrito'),
    path('distritos/inactivar/<str:nombre_distrito>/', views.inactivar_distrito_view, name='inactivar_distrito'),

    ##direccion
    path('direcciones/listar/', views.listar_direcciones_view, name='listar_direcciones'),
    path('direcciones/insertar/', views.insertar_direccion_view, name='insertar_direccion'),
    path('direcciones/actualizar/<int:id_direccion>/', views.actualizar_direccion_view, name='actualizar_direccion'),
    path('direcciones/inactivar/<int:id_direccion>/', views.inactivar_direccion_view, name='inactivar_direccion'),
]
