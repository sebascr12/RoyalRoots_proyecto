from django import forms
from .oracle_service import obtener_estados_disponibles

class MetodoPagoForm(forms.Form):
    nombre = forms.CharField(label='Nombre del Método de Pago', max_length=100)
    estado = forms.ChoiceField(label='Estado')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].choices = [(e, e) for e in obtener_estados_disponibles()]

class ActualizarMetodoPagoForm(forms.Form):
    nuevo_nombre = forms.CharField(label='Nuevo Nombre del Método de Pago', max_length=100)
    nuevo_estado = forms.ChoiceField(label='Nuevo Estado')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nuevo_estado'].choices = [(e, e) for e in obtener_estados_disponibles()]

#historial pago
from .oracle_service import obtener_estados_disponibles, obtener_clientes_disponibles

class HistorialPagoForm(forms.Form):
    cliente = forms.ChoiceField(label='Cliente')
    monto = forms.DecimalField(label='Monto', min_value=0)
    fecha_pago = forms.DateField(label='Fecha de Pago', widget=forms.DateInput(attrs={'type': 'date'}))
    estado = forms.ChoiceField(label='Estado')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].choices = [(c, c) for c in obtener_clientes_disponibles()]
        self.fields['estado'].choices = [(e, e) for e in obtener_estados_disponibles()]

class ActualizarHistorialPagoForm(forms.Form):
    cliente = forms.ChoiceField(label='Cliente')
    monto = forms.DecimalField(label='Monto', min_value=0)
    fecha_pago = forms.DateField(label='Fecha de Pago', widget=forms.DateInput(attrs={'type': 'date'}))
    estado = forms.ChoiceField(label='Estado')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].choices = [(c, c) for c in obtener_clientes_disponibles()]
        self.fields['estado'].choices = [(e, e) for e in obtener_estados_disponibles()]

#facturas
from .oracle_service import obtener_clientes_disponibles, obtener_metodos_pago_disponibles, obtener_estados_disponibles

class FacturaForm(forms.Form):
    cliente = forms.ChoiceField(label='Cliente')
    metodo_pago = forms.ChoiceField(label='Método de Pago')
    fecha_emision = forms.DateField(label='Fecha de Emisión', widget=forms.DateInput(attrs={'type': 'date'}))
    total = forms.DecimalField(label='Total', min_value=0)
    estado = forms.ChoiceField(label='Estado')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].choices = [(c, c) for c in obtener_clientes_disponibles()]
        self.fields['metodo_pago'].choices = [(m, m) for m in obtener_metodos_pago_disponibles()]
        self.fields['estado'].choices = [(e, e) for e in obtener_estados_disponibles()]

class ActualizarFacturaForm(forms.Form):
    total = forms.DecimalField(label='Nuevo Total', min_value=0)
    fecha_emision = forms.DateField(label='Nueva Fecha de Emisión', widget=forms.DateInput(attrs={'type': 'date'}))
    estado = forms.ChoiceField(label='Nuevo Estado')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].choices = [(e, e) for e in obtener_estados_disponibles()]

#detalle facturas
from .oracle_service import obtener_facturas_disponibles, obtener_productos_disponibles, obtener_estados_disponibles

class DetalleFacturaForm(forms.Form):
    factura = forms.ChoiceField(label='Factura')
    producto = forms.ChoiceField(label='Producto')
    subtotal = forms.DecimalField(label='Subtotal', min_value=0)
    estado = forms.ChoiceField(label='Estado')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['factura'].choices = [(f, f) for f in obtener_facturas_disponibles()]
        self.fields['producto'].choices = [(p, p) for p in obtener_productos_disponibles()]
        self.fields['estado'].choices = [(e, e) for e in obtener_estados_disponibles()]

class ActualizarDetalleFacturaForm(forms.Form):
    subtotal = forms.DecimalField(label='Nuevo Subtotal', min_value=0)
    estado = forms.ChoiceField(label='Nuevo Estado')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].choices = [(e, e) for e in obtener_estados_disponibles()]
