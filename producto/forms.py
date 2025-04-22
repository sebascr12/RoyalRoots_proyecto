from django import forms
from .oracle_service import obtener_estados_disponibles

class ProductoForm(forms.Form):
    nombre = forms.CharField(label='Nombre del Producto', max_length=100)
    descripcion = forms.CharField(label='Descripción', max_length=100, widget=forms.Textarea)
    precio = forms.DecimalField(label='Precio Unitario', max_digits=10, decimal_places=2)
    estado = forms.ChoiceField(label='Estado')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].choices = [(e, e) for e in obtener_estados_disponibles()]

class ActualizarProductoForm(forms.Form):
    nuevo_nombre = forms.CharField(label='Nuevo Nombre del Producto', max_length=100)
    nueva_descripcion = forms.CharField(label='Nueva Descripción', max_length=100, widget=forms.Textarea)
    nuevo_precio = forms.DecimalField(label='Nuevo Precio Unitario', max_digits=10, decimal_places=2)
    estado = forms.ChoiceField(label='Nuevo Estado')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].choices = [(e, e) for e in obtener_estados_disponibles()]


##inventario
from .oracle_service import obtener_estados_disponibles, obtener_nombres_productos

class InventarioForm(forms.Form):
    producto = forms.ChoiceField(label='Producto')
    cantidad = forms.IntegerField(label='Cantidad')
    fecha_actualizacion = forms.DateField(
        label='Fecha de Actualización',
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d']
    )
    estado = forms.ChoiceField(label='Estado')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].choices = [(p, p) for p in obtener_nombres_productos()]
        self.fields['estado'].choices = [(e, e) for e in obtener_estados_disponibles()]


#proveedores
from .oracle_service import obtener_estados_disponibles

class ProveedorForm(forms.Form):
    nombre = forms.CharField(label='Nombre del Proveedor', max_length=100)
    contacto = forms.CharField(label='Contacto', max_length=100)
    tipo = forms.CharField(label='Tipo', max_length=100)
    estado = forms.ChoiceField(label='Estado')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].choices = [(e, e) for e in obtener_estados_disponibles()]

class ActualizarProveedorForm(forms.Form):
    nuevo_nombre = forms.CharField(label='Nuevo Nombre del Proveedor', max_length=100)
    nuevo_contacto = forms.CharField(label='Nuevo Contacto', max_length=100)
    nuevo_tipo = forms.CharField(label='Nuevo Tipo', max_length=100)
    estado = forms.ChoiceField(label='Estado')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].choices = [(e, e) for e in obtener_estados_disponibles()]

#ordenes compra
from .oracle_service import obtener_estados_disponibles, obtener_nombres_proveedores

class OrdenCompraForm(forms.Form):
    proveedor = forms.ChoiceField(label='Proveedor')
    fecha_orden = forms.DateField(
        label='Fecha de Orden',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        input_formats=['%Y-%m-%d']
    )
    total = forms.DecimalField(label='Total', max_digits=10, decimal_places=2)
    estado = forms.ChoiceField(label='Estado')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proveedor'].choices = [(p, p) for p in obtener_nombres_proveedores()]
        self.fields['estado'].choices = [(e, e) for e in obtener_estados_disponibles()]


class ActualizarOrdenForm(OrdenCompraForm):
    proveedor = forms.ChoiceField(label='Proveedor')
    fecha_orden = forms.DateField(
        label='Fecha de Orden',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        input_formats=['%Y-%m-%d']
    )
    total = forms.DecimalField(label='Total', max_digits=10, decimal_places=2)
    estado = forms.ChoiceField(label='Estado')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proveedor'].choices = [(p, p) for p in obtener_nombres_proveedores()]
        self.fields['estado'].choices = [(e, e) for e in obtener_estados_disponibles()]
