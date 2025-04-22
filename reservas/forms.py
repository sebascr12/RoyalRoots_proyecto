from django import forms
from reservas.oracle_service import (
    obtener_clientes_disponibles,
    obtener_empleados_disponibles,
    obtener_servicios_disponibles,
    obtener_estados_disponibles
)

class ReservaForm(forms.Form):
    cliente = forms.ChoiceField(label='Cliente')
    empleado = forms.ChoiceField(label='Empleado')
    servicio = forms.ChoiceField(label='Servicio')

    fecha_hora = forms.DateTimeField(
        label='Fecha y Hora',
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'}
        ),
        input_formats=['%Y-%m-%dT%H:%M'],  
    )

    estado = forms.ChoiceField(label='Estado')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].choices = [(c, c) for c in obtener_clientes_disponibles()]
        self.fields['empleado'].choices = [(e, e) for e in obtener_empleados_disponibles()]
        self.fields['servicio'].choices = [(s, s) for s in obtener_servicios_disponibles()]
        self.fields['estado'].choices = [(e, e) for e in obtener_estados_disponibles()]

class ActualizarReservaForm(forms.Form):
    cliente = forms.ChoiceField(label='Cliente')
    empleado = forms.ChoiceField(label='Empleado')
    servicio = forms.ChoiceField(label='Servicio')

    fecha_hora = forms.DateTimeField(
        label='Fecha y Hora',
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'}
        ),
        input_formats=['%Y-%m-%dT%H:%M'],  
    )

    estado = forms.ChoiceField(label='Estado')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].choices = [(c, c) for c in obtener_clientes_disponibles()]
        self.fields['empleado'].choices = [(e, e) for e in obtener_empleados_disponibles()]
        self.fields['servicio'].choices = [(s, s) for s in obtener_servicios_disponibles()]
        self.fields['estado'].choices = [(e, e) for e in obtener_estados_disponibles()]