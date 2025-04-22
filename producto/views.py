from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ProductoForm, ActualizarProductoForm
from .oracle_service import (
    listar_productos,
    insertar_producto,
    actualizar_producto,
    inactivar_producto
)

def listar_productos_view(request):
    productos = listar_productos()
    return render(request, 'producto/listar_productos.html', {'productos': productos})

def insertar_producto_view(request):
    form = ProductoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        success = insertar_producto(data['nombre'], data['descripcion'], float(data['precio']), data['estado'])
        if success:
            messages.success(request, 'Producto insertado correctamente.')
            return redirect('listar_productos')
        messages.error(request, 'Error al insertar el producto.')
    return render(request, 'producto/insertar_producto.html', {'form': form})

def actualizar_producto_view(request, id_producto):
    form = ActualizarProductoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        success = actualizar_producto(
            id_producto, data['nuevo_nombre'], data['nueva_descripcion'],
            float(data['nuevo_precio']), data['estado']
        )
        if success:
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('listar_productos')
        messages.error(request, 'Error al actualizar el producto.')
    return render(request, 'producto/actualizar_producto.html', {
        'form': form, 'id_producto': id_producto
    })

def inactivar_producto_view(request, id_producto):
    success = inactivar_producto(id_producto)
    if success:
        messages.success(request, 'Producto inactivado correctamente.')
    else:
        messages.error(request, 'Error al inactivar el producto.')
    return redirect('listar_productos')

#inventario
from .forms import InventarioForm
from .oracle_service import (
    listar_inventario,
    insertar_inventario,
    actualizar_inventario,
    inactivar_inventario
)

def listar_inventario_view(request):
    inventario = listar_inventario()
    return render(request, 'producto/listar_inventario.html', {'inventario': inventario})

def insertar_inventario_view(request):
    form = InventarioForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        exito = insertar_inventario(data['producto'], data['cantidad'], data['fecha_actualizacion'], data['estado'])
        if exito:
            messages.success(request, "Inventario agregado correctamente.")
            return redirect('listar_inventario')
        messages.error(request, "Error al insertar inventario.")
    return render(request, 'producto/insertar_inventario.html', {'form': form})

def actualizar_inventario_view(request, id_inventario):
    form = InventarioForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        exito = actualizar_inventario(id_inventario, data['producto'], data['cantidad'], data['fecha_actualizacion'], data['estado'])
        if exito:
            messages.success(request, "Inventario actualizado correctamente.")
            return redirect('listar_inventario')
        messages.error(request, "Error al actualizar inventario.")
    return render(request, 'producto/actualizar_inventario.html', {
        'form': form,
        'id_inventario': id_inventario
    })

def inactivar_inventario_view(request, id_inventario):
    exito = inactivar_inventario(id_inventario)
    if exito:
        messages.success(request, "Inventario inactivado correctamente.")
    else:
        messages.error(request, "Error al inactivar inventario.")
    return redirect('listar_inventario')


#proveedores
from .forms import ProveedorForm, ActualizarProveedorForm
from .oracle_service import (
    listar_proveedores,
    insertar_proveedor,
    actualizar_proveedor,
    inactivar_proveedor
)

def listar_proveedores_view(request):
    proveedores = listar_proveedores()
    return render(request, 'producto/listar_proveedores.html', {'proveedores': proveedores})

def insertar_proveedor_view(request):
    form = ProveedorForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        success = insertar_proveedor(
            data['nombre'], data['contacto'], data['tipo'], data['estado']
        )
        if success:
            messages.success(request, 'Proveedor insertado correctamente.')
            return redirect('listar_proveedores')
        else:
            messages.error(request, 'Error al insertar proveedor.')
    return render(request, 'producto/insertar_proveedor.html', {'form': form})

def actualizar_proveedor_view(request, id_proveedor):
    form = ActualizarProveedorForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        success = actualizar_proveedor(
            id_proveedor, data['nuevo_nombre'], data['nuevo_contacto'], data['nuevo_tipo'], data['estado']
        )
        if success:
            messages.success(request, 'Proveedor actualizado correctamente.')
            return redirect('listar_proveedores')
        else:
            messages.error(request, 'Error al actualizar proveedor.')
    return render(request, 'producto/actualizar_proveedor.html', {'form': form, 'id_proveedor': id_proveedor})

def inactivar_proveedor_view(request, id_proveedor):
    success = inactivar_proveedor(id_proveedor)
    if success:
        messages.success(request, 'Proveedor inactivado correctamente.')
    else:
        messages.error(request, 'Error al inactivar proveedor.')
    return redirect('listar_proveedores')

#ordenes compra
from .forms import OrdenCompraForm, ActualizarOrdenForm
from .oracle_service import (
    listar_ordenes_compra,
    insertar_orden_compra,
    actualizar_orden_compra,
    inactivar_orden_compra
)

def listar_ordenes_view(request):
    ordenes = listar_ordenes_compra()
    return render(request, 'producto/listar_ordenes.html', {'ordenes': ordenes})

def insertar_orden_view(request):
    form = OrdenCompraForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        exito = insertar_orden_compra(
            data['proveedor'],
            data['fecha_orden'],
            data['total'],
            data['estado']
        )
        if exito:
            messages.success(request, 'Orden de compra insertada correctamente.')
            return redirect('listar_ordenes')
        else:
            messages.error(request, 'Error al insertar la orden de compra.')
    return render(request, 'producto/insertar_orden.html', {'form': form})

def actualizar_orden_view(request, id_orden):
    form = ActualizarOrdenForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        exito = actualizar_orden_compra(
            id_orden,
            data['proveedor'],
            data['fecha_orden'],
            data['total'],
            data['estado']
        )
        if exito:
            messages.success(request, 'Orden actualizada correctamente.')
            return redirect('listar_ordenes')
        else:
            messages.error(request, 'Error al actualizar la orden.')
    return render(request, 'producto/actualizar_orden.html', {
        'form': form,
        'id_orden': id_orden
    })

def inactivar_orden_view(request, id_orden):
    exito = inactivar_orden_compra(id_orden)
    if exito:
        messages.success(request, 'Orden inactivada correctamente.')
    else:
        messages.error(request, 'Error al inactivar la orden.')
    return redirect('listar_ordenes')