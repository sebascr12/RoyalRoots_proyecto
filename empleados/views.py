from django.shortcuts import render, redirect
from .forms import EmpleadoForm
from django.contrib import messages
from .oracle_service import insertar_empleado, listar_empleados, actualizar_empleado, inactivar_empleado

from .forms import TurnoForm
from .forms import ActualizarTurnoForm
from .oracle_service import insertar_turno, listar_turnos, actualizar_turno, eliminar_turno
from datetime import datetime
from django.utils.dateparse import parse_time

from .oracle_service import insertar_funcion,listar_funciones,actualizar_funcion,inactivar_funcion
from .forms import FuncionForm, ActualizarFuncionForm

from .forms import EmpleadoForm
from .oracle_service import (
    listar_empleados,
    insertar_empleado,
    actualizar_empleado,
    inactivar_empleado
)

# Listar empleados
def empleados_list_view(request):
    empleados = listar_empleados()
    return render(request, 'empleados/listar.html', {'empleados': empleados})

# Agregar empleado
def agregar_empleado_view(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            turno_inicio, turno_fin = form.cleaned_data['turno'].split('-')
            success = insertar_empleado(
                form.cleaned_data['nombre'],
                form.cleaned_data['apellido'],
                form.cleaned_data['correo'],
                form.cleaned_data['telefono'],
                form.cleaned_data['fecha_contratacion'],
                form.cleaned_data['salario'],
                form.cleaned_data['funcion'],
                turno_inicio.strip(),
                turno_fin.strip(),
                form.cleaned_data['estado']
            )
            if success:
                messages.success(request, 'Empleado insertado correctamente.')
                return redirect('empleados_list')
            else:
                messages.error(request, 'Hubo un error al insertar el empleado.')
    else:
        form = EmpleadoForm()
    return render(request, 'empleados/insertar.html', {'form': form})

# Editar empleado
def editar_empleado_view(request, correo):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            turno_inicio, turno_fin = form.cleaned_data['turno'].split('-')
            success = actualizar_empleado(
                form.cleaned_data['nombre'],
                form.cleaned_data['apellido'],
                correo,
                form.cleaned_data['telefono'],
                form.cleaned_data['fecha_contratacion'],
                form.cleaned_data['salario'],
                form.cleaned_data['funcion'],
                turno_inicio.strip(),
                turno_fin.strip(),
                form.cleaned_data['estado']
            )
            if success:
                messages.success(request, 'Empleado actualizado correctamente.')
                return redirect('empleados_list')
            else:
                messages.error(request, 'Error al actualizar el empleado.')
    else:
        # Inicialización del formulario para edición (solo correo pre-cargado)
        form = EmpleadoForm(initial={'correo': correo})
    return render(request, 'empleados/insertar.html', {'form': form, 'editar': True})

# Inactivar empleado
def inactivar_empleado_view(request, correo):
    if inactivar_empleado(correo):
        messages.success(request, 'Empleado inactivado correctamente.')
    else:
        messages.error(request, 'Error al inactivar el empleado.')
    return redirect('empleados_list')

##turnos

def listar_turnos_view(request):
    turnos = listar_turnos()
    return render(request, 'empleados/listar_turnos.html', {'turnos': turnos})


def insertar_turno_view(request):
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            hora_inicio = form.cleaned_data['hora_inicio'].strftime('%H:%M')
            hora_fin = form.cleaned_data['hora_fin'].strftime('%H:%M')
            estado = form.cleaned_data['estado']
            if insertar_turno(hora_inicio, hora_fin, estado):
                messages.success(request, 'Turno insertado correctamente.')
                return redirect('listar_turnos')  # Corrigido
            else:
                messages.error(request, 'Error al insertar el turno.')
    else:
        form = TurnoForm()
    return render(request, 'empleados/insertar_turno.html', {'form': form})


def actualizar_turno_view(request, hora_inicio, hora_fin):
    if request.method == 'POST':
        form = ActualizarTurnoForm(request.POST)
        if form.is_valid():
            nueva_hora_inicio = form.cleaned_data['nueva_hora_inicio'].strftime('%H:%M')
            nueva_hora_fin = form.cleaned_data['nueva_hora_fin'].strftime('%H:%M')
            estado = form.cleaned_data['estado']
            if actualizar_turno(hora_inicio, hora_fin, nueva_hora_inicio, nueva_hora_fin, estado):
                messages.success(request, 'Turno actualizado correctamente.')
                return redirect('listar_turnos')  # Corrigido
            else:
                messages.error(request, 'Error al actualizar el turno.')
    else:
        form = ActualizarTurnoForm(initial={
            'nueva_hora_inicio': hora_inicio,
            'nueva_hora_fin': hora_fin,
        })
    return render(request, 'empleados/actualizar_turno.html', {
        'form': form,
        'hora_inicio': hora_inicio,
        'hora_fin': hora_fin
    })


def eliminar_turno_view(request, hora_inicio, hora_fin):
    if eliminar_turno(hora_inicio, hora_fin):
        messages.success(request, 'Turno inactivado correctamente.')
    else:
        messages.error(request, 'Error al inactivar el turno.')
    return redirect('listar_turnos') 


##funciones

def listar_funciones_view(request):
    funciones = listar_funciones()
    return render(request, 'empleados/listar_funciones.html', {'funciones': funciones})

def insertar_funcion_view(request):
    if request.method == 'POST':
        form = FuncionForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre_funcion']
            descripcion = form.cleaned_data['descripcion']
            estado = form.cleaned_data['estado']
            if insertar_funcion(nombre, descripcion, estado):
                messages.success(request, 'Función insertada correctamente.')
                return redirect('listar_funciones')
            else:
                messages.error(request, 'Error al insertar la función.')
    else:
        form = FuncionForm()
    return render(request, 'empleados/insertar_funcion.html', {'form': form})

def actualizar_funcion_view(request, nombre_funcion):  # ← antes decía nombre_actual
    if request.method == 'POST':
        form = ActualizarFuncionForm(request.POST)
        if form.is_valid():
            nuevo_nombre = form.cleaned_data['nuevo_nombre']
            descripcion = form.cleaned_data['descripcion']
            estado = form.cleaned_data['estado']
            if actualizar_funcion(nombre_funcion, nuevo_nombre, descripcion, estado):
                messages.success(request, 'Función actualizada correctamente.')
                return redirect('listar_funciones')
            else:
                messages.error(request, 'Error al actualizar la función.')
    else:
        form = ActualizarFuncionForm(initial={'nuevo_nombre': nombre_funcion})
    return render(request, 'empleados/actualizar_funcion.html', {
        'form': form,
        'nombre_actual': nombre_funcion
    })

def inactivar_funcion_view(request, nombre_funcion):
    if inactivar_funcion(nombre_funcion):
        messages.success(request, f'Función "{nombre_funcion}" inactivada correctamente.')
    else:
        messages.error(request, f'Error al inactivar la función "{nombre_funcion}".')
    return redirect('listar_funciones')
