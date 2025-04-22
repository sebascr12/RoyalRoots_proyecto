from django.urls import path
from . import views

urlpatterns = [
    path('reservas/listar/', views.listar_reservas_view, name='listar_reservas'),
    path('reservas/insertar/', views.insertar_reserva_view, name='insertar_reserva'),
    path('reservas/actualizar/<int:id_reserva>/', views.actualizar_reserva_view, name='actualizar_reserva'),
    path('reservas/inactivar/<int:id_reserva>/', views.inactivar_reserva_view, name='inactivar_reserva'),
]