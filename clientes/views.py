from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ServicioForm, ActualizarServicioForm
from clientes.oracle_service import (
    insertar_servicio,
    listar_servicios,
    actualizar_servicio,
    inactivar_servicio
)

from .forms import BeneficioForm, ActualizarBeneficioForm
from clientes.oracle_service import (
    insertar_beneficio,
    listar_beneficios,
    actualizar_beneficio,
    inactivar_beneficio
)


from .forms import ClienteForm, ActualizarClienteForm
from .oracle_service import (
    listar_clientes,
    insertar_cliente,
    actualizar_cliente,
    inactivar_cliente
)

# Vista para listar servicios
def listar_servicios_view(request):
    servicios = listar_servicios()
    return render(request, 'clientes/listar_servicios.html', {'servicios': servicios})

# Vista para insertar un nuevo servicio
def insertar_servicio_view(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            success = insertar_servicio(
                form.cleaned_data['nombre'],
                form.cleaned_data['descripcion'],
                form.cleaned_data['precio'],
                form.cleaned_data['estado']
            )
            if success:
                messages.success(request, "Servicio insertado correctamente.")
                return redirect('listar_servicios')
            else:
                messages.error(request, "Error al insertar el servicio.")
    else:
        form = ServicioForm()
    return render(request, 'clientes/insertar_servicio.html', {'form': form})

# Vista para actualizar un servicio
def actualizar_servicio_view(request, nombre_actual):
    if request.method == 'POST':
        form = ActualizarServicioForm(request.POST)
        if form.is_valid():
            success = actualizar_servicio(
                nombre_actual,
                form.cleaned_data['nuevo_nombre'],
                form.cleaned_data['descripcion'],
                form.cleaned_data['precio'],
                form.cleaned_data['estado']
            )
            if success:
                messages.success(request, "Servicio actualizado correctamente.")
                return redirect('listar_servicios')
            else:
                messages.error(request, "Error al actualizar el servicio.")
    else:
        form = ActualizarServicioForm(initial={'nuevo_nombre': nombre_actual})
    return render(request, 'clientes/actualizar_servicio.html', {
        'form': form,
        'nombre_actual': nombre_actual
    })

# Vista para inactivar servicio
def inactivar_servicio_view(request, nombre_servicio):
    success = inactivar_servicio(nombre_servicio)
    if success:
        messages.success(request, "Servicio inactivado correctamente.")
    else:
        messages.error(request, "Error al inactivar el servicio.")
    return redirect('listar_servicios')

#beneficios
def listar_beneficios_view(request):
    beneficios = listar_beneficios()
    return render(request, 'clientes/listar_beneficios.html', {'beneficios': beneficios})

def insertar_beneficio_view(request):
    if request.method == 'POST':
        form = BeneficioForm(request.POST)
        if form.is_valid():
            detalle = form.cleaned_data['detalle_beneficio']
            servicio = form.cleaned_data['servicio']
            estado = form.cleaned_data['estado']
            if insertar_beneficio(detalle, servicio, estado):
                messages.success(request, 'Beneficio insertado correctamente.')
                return redirect('listar_beneficios')
            else:
                messages.error(request, 'Error al insertar beneficio.')
    else:
        form = BeneficioForm()
    return render(request, 'clientes/insertar_beneficio.html', {'form': form})

def actualizar_beneficio_view(request, detalle_actual):
    if request.method == 'POST':
        form = ActualizarBeneficioForm(request.POST)
        if form.is_valid():
            nuevo_detalle = form.cleaned_data['nuevo_detalle']
            nuevo_servicio = form.cleaned_data['nuevo_servicio']
            nuevo_estado = form.cleaned_data['nuevo_estado']
            if actualizar_beneficio(detalle_actual, nuevo_detalle, nuevo_servicio, nuevo_estado):
                messages.success(request, 'Beneficio actualizado correctamente.')
                return redirect('listar_beneficios')
            else:
                messages.error(request, 'Error al actualizar el beneficio.')
    else:
        form = ActualizarBeneficioForm(initial={'nuevo_detalle': detalle_actual})
    return render(request, 'clientes/actualizar_beneficio.html', {
        'form': form,
        'detalle_actual': detalle_actual
    })

def inactivar_beneficio_view(request, detalle_beneficio):
    if inactivar_beneficio(detalle_beneficio):
        messages.success(request, 'Beneficio inactivado correctamente.')
    else:
        messages.error(request, 'Error al inactivar el beneficio.')
    return redirect('listar_beneficios')

##clientes
# Vista para listar clientes
def listar_clientes_view(request):
    clientes = listar_clientes()
    return render(request, 'clientes/listar_clientes.html', {'clientes': clientes})


# Vista para insertar cliente
def insertar_cliente_view(request):
    form = ClienteForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
            success = insertar_cliente(
                data['nombre'],
                data['telefono'],
                data['correo'],
                data['fecha_registro'].strftime('%d/%m/%Y'),
                data['direccion'],
                data['estado']
            )
            if success:
                messages.success(request, 'Cliente insertado correctamente.')
                return redirect('listar_clientes')
            else:
                messages.error(request, 'Error al insertar cliente.')
    return render(request, 'clientes/insertar_cliente.html', {'form': form})


# Vista para actualizar cliente
def actualizar_cliente_view(request, id_cliente):
    if request.method == 'POST':
        form = ActualizarClienteForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            success = actualizar_cliente(
                id_cliente,
                data['nombre'],
                data['telefono'],
                data['correo'],
                data['fecha_registro'].strftime('%d/%m/%Y'),
                data['direccion'],
                data['estado']
            )
            if success:
                messages.success(request, 'Cliente actualizado correctamente.')
                return redirect('listar_clientes')
            else:
                messages.error(request, 'Error al actualizar cliente.')
    else:
        # Si deseas precargar el formulario, podrías obtener los datos del cliente aquí con otra función
        form = ActualizarClienteForm()
    return render(request, 'clientes/actualizar_cliente.html', {
        'form': form,
        'id_cliente': id_cliente
    })


# Vista para inactivar cliente
def inactivar_cliente_view(request, id_cliente):
    success = inactivar_cliente(id_cliente)
    if success:
        messages.success(request, 'Cliente inactivado correctamente.')
    else:
        messages.error(request, 'Error al inactivar cliente.')
    return redirect('listar_clientes')