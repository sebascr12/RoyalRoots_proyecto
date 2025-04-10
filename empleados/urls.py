from django.urls import path
from . import views

urlpatterns = [
    path('listar/', views.empleados_list_view, name='empleados_list'),
    path('agregar/', views.agregar_empleado_view, name='agregar_empleado'),
    path('editar/<str:correo>/', views.editar_empleado_view, name='editar_empleado'),
    path('inactivar/<str:correo>/', views.inactivar_empleado_view, name='inactivar_empleado'),

    ##turnos
    path('empleados/listar/', views.listar_turnos_view, name='listar_turnos'),
    path('empleados/insertar/', views.insertar_turno_view, name='insertar_turno'),
    path('empleados/actualizar/<str:hora_inicio>/<str:hora_fin>/', views.actualizar_turno_view, name='actualizar_turno'),
    path('empleados/inactivar/<str:hora_inicio>/<str:hora_fin>/', views.eliminar_turno_view, name='inactivar_turno'),
    ##funciones
    path('funciones/listar/', views.listar_funciones_view, name='listar_funciones'),
    path('funciones/insertar/', views.insertar_funcion_view, name='insertar_funcion'),
    path('funciones/actualizar/<str:nombre_funcion>/', views.actualizar_funcion_view, name='actualizar_funcion'),
    path('funciones/inactivar/<str:nombre_funcion>/', views.inactivar_funcion_view, name='inactivar_funcion'),
]