from django.urls import path
from . import views

urlpatterns = [
    # otras rutas...
    path('reportes/', views.reportes_view, name='reportes'),
]
