from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import MetodoPagoForm, ActualizarMetodoPagoForm
from .oracle_service import (
    listar_metodos_pago,
    insertar_metodo_pago,
    actualizar_metodo_pago,
    inactivar_metodo_pago
)

def listar_metodos_pago_view(request):
    metodos = listar_metodos_pago()
    return render(request, 'facturacion/listar_metodos_pago.html', {'metodos': metodos})

def insertar_metodo_pago_view(request):
    form = MetodoPagoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        exito = insertar_metodo_pago(data['nombre'], data['estado'])
        if exito:
            messages.success(request, 'Método de pago insertado correctamente.')
            return redirect('listar_metodos_pago')
        messages.error(request, 'Error al insertar el método de pago.')
    return render(request, 'facturacion/insertar_metodo_pago.html', {'form': form})

def actualizar_metodo_pago_view(request, id_metodo):
    form = ActualizarMetodoPagoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        exito = actualizar_metodo_pago(id_metodo, data['nuevo_nombre'], data['nuevo_estado'])
        if exito:
            messages.success(request, 'Método de pago actualizado correctamente.')
            return redirect('listar_metodos_pago')
        messages.error(request, 'Error al actualizar el método de pago.')
    return render(request, 'facturacion/actualizar_metodo_pago.html', {
        'form': form, 'id_metodo': id_metodo
    })

def inactivar_metodo_pago_view(request, id_metodo):
    exito = inactivar_metodo_pago(id_metodo)
    if exito:
        messages.success(request, 'Método de pago inactivado correctamente.')
    else:
        messages.error(request, 'Error al inactivar el método de pago.')
    return redirect('listar_metodos_pago')


#historial pago
from .forms import HistorialPagoForm, ActualizarHistorialPagoForm
from .oracle_service import (
    listar_historial_pagos,
    insertar_historial_pago,
    actualizar_historial_pago,
    inactivar_historial_pago
)

def listar_historial_pagos_view(request):
    pagos = listar_historial_pagos()
    return render(request, 'facturacion/listar_historial_pagos.html', {'pagos': pagos})

def insertar_historial_pago_view(request):
    form = HistorialPagoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        exito = insertar_historial_pago(
            data['cliente'], data['monto'], data['fecha_pago'], data['estado']
        )
        if exito:
            messages.success(request, 'Pago registrado correctamente.')
            return redirect('listar_historial_pagos')
        messages.error(request, 'Error al registrar el pago.')
    return render(request, 'facturacion/insertar_historial_pago.html', {'form': form})

def actualizar_historial_pago_view(request, id_pago):
    form = ActualizarHistorialPagoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        exito = actualizar_historial_pago(
            id_pago, data['monto'], data['fecha_pago'], data['estado']
        )
        if exito:
            messages.success(request, 'Pago actualizado correctamente.')
            return redirect('listar_historial_pagos')
        messages.error(request, 'Error al actualizar el pago.')
    return render(request, 'facturacion/actualizar_historial_pago.html', {
        'form': form, 'id_pago': id_pago
    })

def inactivar_historial_pago_view(request, id_pago):
    exito = inactivar_historial_pago(id_pago)
    if exito:
        messages.success(request, 'Pago inactivado correctamente.')
    else:
        messages.error(request, 'Error al inactivar el pago.')
    return redirect('listar_historial_pagos')

#facturas
from .forms import FacturaForm, ActualizarFacturaForm
from .oracle_service import (
    listar_facturas,
    insertar_factura,
    actualizar_factura,
    inactivar_factura
)

def listar_facturas_view(request):
    facturas = listar_facturas()
    return render(request, 'facturacion/listar_facturas.html', {'facturas': facturas})

def insertar_factura_view(request):
    form = FacturaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        exito = insertar_factura(
            data['cliente'], data['metodo_pago'], data['fecha_emision'], data['total'], data['estado']
        )
        if exito:
            messages.success(request, 'Factura insertada correctamente.')
            return redirect('listar_facturas')
        messages.error(request, 'Error al insertar la factura.')
    return render(request, 'facturacion/insertar_factura.html', {'form': form})

def actualizar_factura_view(request, id_factura):
    form = ActualizarFacturaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        exito = actualizar_factura(id_factura, data['total'], data['fecha_emision'], data['estado'])
        if exito:
            messages.success(request, 'Factura actualizada correctamente.')
            return redirect('listar_facturas')
        messages.error(request, 'Error al actualizar la factura.')
    return render(request, 'facturacion/actualizar_factura.html', {
        'form': form, 'id_factura': id_factura
    })

def inactivar_factura_view(request, id_factura):
    exito = inactivar_factura(id_factura)
    if exito:
        messages.success(request, 'Factura inactivada correctamente.')
    else:
        messages.error(request, 'Error al inactivar la factura.')
    return redirect('listar_facturas')


#detalle facturas

from .forms import DetalleFacturaForm, ActualizarDetalleFacturaForm
from .oracle_service import (
    listar_detalles_factura,
    insertar_detalle_factura,
    actualizar_detalle_factura,
    inactivar_detalle_factura
)

def listar_detalles_factura_view(request):
    detalles = listar_detalles_factura()
    return render(request, 'facturacion/listar_detalles_factura.html', {'detalles': detalles})

def insertar_detalle_factura_view(request):
    form = DetalleFacturaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        exito = insertar_detalle_factura(data['factura'], data['producto'], data['subtotal'], data['estado'])
        if exito:
            messages.success(request, 'Detalle de factura insertado correctamente.')
            return redirect('listar_detalles_factura')
        messages.error(request, 'Error al insertar el detalle.')
    return render(request, 'facturacion/insertar_detalle_factura.html', {'form': form})

def actualizar_detalle_factura_view(request, id_detalle):
    form = ActualizarDetalleFacturaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        exito = actualizar_detalle_factura(id_detalle, data['subtotal'], data['estado'])
        if exito:
            messages.success(request, 'Detalle de factura actualizado correctamente.')
            return redirect('listar_detalles_factura')
        messages.error(request, 'Error al actualizar el detalle.')
    return render(request, 'facturacion/actualizar_detalle_factura.html', {
        'form': form, 'id_detalle': id_detalle
    })

def inactivar_detalle_factura_view(request, id_detalle):
    exito = inactivar_detalle_factura(id_detalle)
    if exito:
        messages.success(request, 'Detalle de factura inactivado correctamente.')
    else:
        messages.error(request, 'Error al inactivar el detalle.')
    return redirect('listar_detalles_factura')
