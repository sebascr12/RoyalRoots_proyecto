from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime


from .forms import ReservaForm, ActualizarReservaForm
from .oracle_service import (
    listar_reservas,
    insertar_reserva,
    actualizar_reserva,
    inactivar_reserva
)

def listar_reservas_view(request):
    reservas = listar_reservas()
    return render(request, 'reservas/listar_reservas.html', {'reservas': reservas})


def insertar_reserva_view(request):
    form = ReservaForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
            exito = insertar_reserva(
                data['cliente'],
                data['empleado'],
                data['servicio'],
                data['fecha_hora'].strftime('%d/%m/%Y %H:%M'),
                data['estado']
            )
            if exito:
                messages.success(request, 'Reserva creada correctamente.')
                return redirect('listar_reservas')
            else:
                messages.error(request, 'Ocurrió un error al crear la reserva.')
    return render(request, 'reservas/insertar_reserva.html', {'form': form})



def actualizar_reserva_view(request, id_reserva):
    form = ActualizarReservaForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
            exito = actualizar_reserva(
                id_reserva,
                data['cliente'],
                data['empleado'],
                data['servicio'],
                data['fecha_hora'].strftime('%d/%m/%Y %H:%M'),
                data['estado']
            )
            if exito:
                messages.success(request, 'Reserva actualizada correctamente.')
                return redirect('listar_reservas')
            else:
                messages.error(request, 'Ocurrió un error al actualizar la reserva.')
    return render(request, 'reservas/actualizar_reserva.html', {
        'form': form,
        'id_reserva': id_reserva,
    })

def inactivar_reserva_view(request, id_reserva):
    exito = inactivar_reserva(id_reserva)
    if exito:
        messages.success(request, 'Reserva inactivada correctamente.')
    else:
        messages.error(request, 'Ocurrió un error al inactivar la reserva.')
    return redirect('listar_reservas')