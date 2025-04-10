from django import forms
from clientes.oracle_service import obtener_estados_disponibles, obtener_servicios_disponibles

from clientes.oracle_service import (
    obtener_estados_disponibles,
    obtener_servicios_disponibles,
    generar_direcciones_disponibles
)
from direcciones.oracle_service import (
    obtener_provincias_disponibles,
    obtener_cantones_disponibles,
    obtener_distritos_disponibles,
    obtener_estados_disponibles,
)

# Formulario para insertar un nuevo servicio
class ServicioForm(forms.Form):
    nombre = forms.CharField(label="Nombre del Servicio", max_length=100)
    descripcion = forms.CharField(label="Descripción", max_length=100, widget=forms.Textarea)
    precio = forms.DecimalField(label="Precio", max_digits=10, decimal_places=2)
    estado = forms.ChoiceField(label="Estado")

    def __init__(self, *args, **kwargs):
        super(ServicioForm, self).__init__(*args, **kwargs)
        self.fields['estado'].choices = [(e, e) for e in obtener_estados_disponibles()]

# Formulario para actualizar un servicio
class ActualizarServicioForm(forms.Form):
    nuevo_nombre = forms.CharField(label="Nuevo Nombre", max_length=100)
    descripcion = forms.CharField(label="Nueva Descripción", max_length=100, widget=forms.Textarea)
    precio = forms.DecimalField(label="Nuevo Precio", max_digits=10, decimal_places=2)
    estado = forms.ChoiceField(label="Nuevo Estado")

    def __init__(self, *args, **kwargs):
        super(ActualizarServicioForm, self).__init__(*args, **kwargs)
        self.fields['estado'].choices = [(e, e) for e in obtener_estados_disponibles()]

##beneficios

class BeneficioForm(forms.Form):
    detalle_beneficio = forms.CharField(label='Detalle del Beneficio', max_length=100)
    servicio = forms.ChoiceField(label='Servicio')
    estado = forms.ChoiceField(label='Estado')

    def __init__(self, *args, **kwargs):
        super(BeneficioForm, self).__init__(*args, **kwargs)
        self.fields['servicio'].choices = [(s, s) for s in obtener_servicios_disponibles()]
        self.fields['estado'].choices = [(e, e) for e in obtener_estados_disponibles()]

class ActualizarBeneficioForm(forms.Form):
    nuevo_detalle = forms.CharField(label='Nuevo Detalle del Beneficio', max_length=100)
    nuevo_servicio = forms.ChoiceField(label='Nuevo Servicio')
    nuevo_estado = forms.ChoiceField(label='Nuevo Estado')

    def __init__(self, *args, **kwargs):
        super(ActualizarBeneficioForm, self).__init__(*args, **kwargs)
        self.fields['nuevo_servicio'].choices = [(s, s) for s in obtener_servicios_disponibles()]
        self.fields['nuevo_estado'].choices = [(e, e) for e in obtener_estados_disponibles()]

##clientes

class ClienteForm(forms.Form):
    nombre = forms.CharField(label='Nombre del Cliente', max_length=100)
    telefono = forms.CharField(label='Teléfono', max_length=100)
    correo = forms.EmailField(label='Correo', max_length=200)
    fecha_registro = forms.DateField(
        label='Fecha de Registro',
        input_formats=['%d/%m/%Y'],
        widget=forms.TextInput(attrs={'placeholder': 'DD/MM/YYYY'})
    )
    direccion = forms.ChoiceField(label='Dirección')
    estado = forms.ChoiceField(label='Estado')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['direccion'].choices = [(d, d) for d in generar_direcciones_disponibles()]
        self.fields['estado'].choices = [(e, e) for e in obtener_estados_disponibles()]


class ActualizarClienteForm(forms.Form):
    nombre = forms.CharField(label='Nombre del Cliente', max_length=100)
    telefono = forms.CharField(label='Teléfono', max_length=100)
    correo = forms.EmailField(label='Correo', max_length=200)
    fecha_registro = forms.DateField(
        label='Fecha de Registro',
        input_formats=['%d/%m/%Y'],
        widget=forms.TextInput(attrs={'placeholder': 'DD/MM/YYYY'})
    )
    direccion = forms.ChoiceField(label='Dirección')
    estado = forms.ChoiceField(label='Estado')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['direccion'].choices = [(d, d) for d in generar_direcciones_disponibles()]
        self.fields['estado'].choices = [(e, e) for e in obtener_estados_disponibles()]