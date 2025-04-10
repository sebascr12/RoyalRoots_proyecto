from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import (
    ProvinciaForm, ActualizarProvinciaForm,
    CantonForm, ActualizarCantonForm,
    DistritoForm, ActualizarDistritoForm,
    DireccionForm, ActualizarDireccionForm
)
from .oracle_service import (
    insertar_provincia, listar_provincias, actualizar_provincia, inactivar_provincia,
    insertar_canton, listar_cantones, actualizar_canton, inactivar_canton,
    insertar_distrito, listar_distritos, actualizar_distrito, inactivar_distrito,
    listar_direcciones, insertar_direccion, actualizar_direccion, inactivar_direccion
)

# PROVINCIAS
def listar_provincias_view(request):
    provincias = listar_provincias()
    return render(request, 'direcciones/listar_provincias.html', {'provincias': provincias})

def insertar_provincia_view(request):
    form = ProvinciaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        nombre = form.cleaned_data['provincia'].upper()
        estado = form.cleaned_data['estado'].upper()
        if insertar_provincia(nombre, estado):
            messages.success(request, 'Provincia insertada correctamente.')
            return redirect('listar_provincias')
        messages.error(request, 'Error al insertar la provincia.')
    return render(request, 'direcciones/insertar_provincia.html', {'form': form})

def actualizar_provincia_view(request, nombre_actual):
    form = ActualizarProvinciaForm(request.POST or None, initial={'nuevo_nombre': nombre_actual})
    if request.method == 'POST' and form.is_valid():
        nueva_provincia = form.cleaned_data['nuevo_nombre'].upper()
        estado = form.cleaned_data['estado'].upper()
        if actualizar_provincia(nombre_actual.upper(), nueva_provincia, estado):
            messages.success(request, 'Provincia actualizada correctamente.')
            return redirect('listar_provincias')
        messages.error(request, 'Error al actualizar la provincia.')
    return render(request, 'direcciones/actualizar_provincia.html', {'form': form, 'nombre_actual': nombre_actual})

def inactivar_provincia_view(request, nombre_provincia):
    if inactivar_provincia(nombre_provincia.upper()):
        messages.success(request, f'Provincia "{nombre_provincia}" inactivada correctamente.')
    else:
        messages.error(request, f'Error al inactivar la provincia "{nombre_provincia}".')
    return redirect('listar_provincias')

# CANTONES
def listar_cantones_view(request):
    cantones = listar_cantones()
    return render(request, 'direcciones/listar_cantones.html', {'cantones': cantones})

def insertar_canton_view(request):
    form = CantonForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        canton = form.cleaned_data['canton'].upper()
        provincia = form.cleaned_data['provincia'].upper()
        estado = form.cleaned_data['estado'].upper()
        if insertar_canton(canton, provincia, estado):
            messages.success(request, 'Cantón insertado correctamente.')
            return redirect('listar_cantones')
        messages.error(request, 'Error al insertar el cantón.')
    return render(request, 'direcciones/insertar_canton.html', {'form': form})

def actualizar_canton_view(request, nombre_actual):
    form = ActualizarCantonForm(request.POST or None, initial={'nuevo_nombre': nombre_actual})
    if request.method == 'POST' and form.is_valid():
        nuevo_nombre = form.cleaned_data['nuevo_nombre'].upper()
        nueva_provincia = form.cleaned_data['provincia'].upper()
        nuevo_estado = form.cleaned_data['estado'].upper()
        if actualizar_canton(nombre_actual.upper(), nuevo_nombre, nueva_provincia, nuevo_estado):
            messages.success(request, 'Cantón actualizado correctamente.')
            return redirect('listar_cantones')
        messages.error(request, 'Error al actualizar el cantón.')
    return render(request, 'direcciones/actualizar_canton.html', {'form': form, 'nombre_actual': nombre_actual})

def inactivar_canton_view(request):
    nombre_canton = request.GET.get('nombre', '').upper()
    if nombre_canton:
        if inactivar_canton(nombre_canton):
            messages.success(request, f'Cantón "{nombre_canton}" inactivado correctamente.')
        else:
            messages.error(request, f'Error al inactivar el cantón "{nombre_canton}".')
    else:
        messages.error(request, 'No se proporcionó el nombre del cantón.')
    return redirect('listar_cantones')

# DISTRITOS
def listar_distritos_view(request):
    distritos = listar_distritos()
    return render(request, 'direcciones/listar_distritos.html', {'distritos': distritos})

def insertar_distrito_view(request):
    form = DistritoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        nombre = form.cleaned_data['distrito'].upper()
        canton = form.cleaned_data['canton'].upper()
        estado = form.cleaned_data['estado'].upper()
        if insertar_distrito(nombre, canton, estado):
            messages.success(request, 'Distrito insertado correctamente.')
            return redirect('listar_distritos')
        messages.error(request, 'Error al insertar el distrito.')
    return render(request, 'direcciones/insertar_distrito.html', {'form': form})

def actualizar_distrito_view(request, nombre_actual):
    form = ActualizarDistritoForm(request.POST or None, initial={'nuevo_nombre': nombre_actual})
    if request.method == 'POST' and form.is_valid():
        nuevo_nombre = form.cleaned_data['nuevo_nombre'].upper()
        nuevo_canton = form.cleaned_data['canton'].upper()
        nuevo_estado = form.cleaned_data['estado'].upper()
        if actualizar_distrito(nombre_actual.upper(), nuevo_nombre, nuevo_canton, nuevo_estado):
            messages.success(request, 'Distrito actualizado correctamente.')
            return redirect('listar_distritos')
        messages.error(request, 'Error al actualizar el distrito.')
    return render(request, 'direcciones/actualizar_distrito.html', {'form': form, 'nombre_actual': nombre_actual})

def inactivar_distrito_view(request, nombre_distrito):
    if inactivar_distrito(nombre_distrito.upper()):
        messages.success(request, f'Distrito "{nombre_distrito}" inactivado correctamente.')
    else:
        messages.error(request, f'Error al inactivar el distrito "{nombre_distrito}".')
    return redirect('listar_distritos')

# DIRECCIONES
def listar_direcciones_view(request):
    direcciones = listar_direcciones()
    return render(request, 'direcciones/listar_direcciones.html', {'direcciones': direcciones})

def insertar_direccion_view(request):
    form = DireccionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        exito = insertar_direccion(
            data['provincia'].upper(),
            data['canton'].upper(),
            data['distrito'].upper(),
            data['estado'].upper()
        )
        if exito:
            messages.success(request, 'Dirección insertada correctamente.')
            return redirect('listar_direcciones')
        messages.error(request, 'Ocurrió un error al insertar la dirección.')
    return render(request, 'direcciones/insertar_direccion.html', {'form': form})

def actualizar_direccion_view(request, id_direccion):
    form = ActualizarDireccionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        exito = actualizar_direccion(
            id_direccion,
            data['nueva_provincia'].upper(),
            data['nuevo_canton'].upper(),
            data['nuevo_distrito'].upper(),
            data['nuevo_estado'].upper()
        )
        if exito:
            messages.success(request, 'Dirección actualizada correctamente.')
            return redirect('listar_direcciones')
        messages.error(request, 'Ocurrió un error al actualizar la dirección.')
    return render(request, 'direcciones/actualizar_direccion.html', {
        'form': form,
        'id_direccion': id_direccion
    })

def inactivar_direccion_view(request, id_direccion):
    if inactivar_direccion(id_direccion):
        messages.success(request, 'Dirección inactivada correctamente.')
    else:
        messages.error(request, 'Ocurrió un error al inactivar la dirección.')
    return redirect('listar_direcciones')
