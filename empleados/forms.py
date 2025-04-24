from django import forms

from datetime import date

from empleados.oracle_service import (
    obtener_funciones_disponibles,
    obtener_estados_disponibles,
    obtener_turnos_disponibles
)

class EmpleadoForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100)
    apellido = forms.CharField(label='Apellido', max_length=100)
    correo = forms.EmailField(label='Correo')
    telefono = forms.CharField(label='Teléfono', max_length=20)
    fecha_contratacion = forms.DateField(label='Fecha de Contratación', widget=forms.DateInput(attrs={'type': 'date'}))
    salario = forms.DecimalField(label='Salario', max_digits=10, decimal_places=2)

    funcion = forms.ChoiceField(label='Función')
    estado = forms.ChoiceField(label='Estado')
    turno = forms.ChoiceField(label='Turno')  # Se muestra como "08:00 - 16:00"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        funciones = obtener_funciones_disponibles()
        self.fields['funcion'].choices = [(f, f) for f in funciones]

        estados = obtener_estados_disponibles()
        self.fields['estado'].choices = [(e, e) for e in estados]

        turnos = obtener_turnos_disponibles()
        self.fields['turno'].choices = [
            (f"{inicio}-{fin}", f"{inicio} - {fin}") for inicio, fin in turnos
        ]


class TurnoForm(forms.Form):
    hora_inicio = forms.TimeField(label='Hora de inicio', widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}))
    hora_fin = forms.TimeField(label='Hora de fin', widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}))
    estado = forms.CharField(label='Estado', max_length=50)


class ActualizarTurnoForm(forms.Form):
    nueva_hora_inicio = forms.TimeField(label='Nueva hora de inicio', widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}))
    nueva_hora_fin = forms.TimeField(label='Nueva hora de fin', widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}))
    estado = forms.CharField(label='Nuevo estado', max_length=50)



ESTADOS_CHOICES = [
    ('ACTIVO', 'ACTIVO'),
    ('INACTIVO', 'INACTIVO'),
]

class FuncionForm(forms.Form):
    nombre_funcion = forms.CharField(label='Nombre de la Función', max_length=100)
    descripcion = forms.CharField(label='Descripción', max_length=100)
    estado = forms.ChoiceField(choices=ESTADOS_CHOICES, label='Estado')

class ActualizarFuncionForm(forms.Form):
    nuevo_nombre = forms.CharField(label='Nuevo Nombre de la Función', max_length=100)
    descripcion = forms.CharField(label='Nueva Descripción', max_length=100)
    estado = forms.ChoiceField(choices=ESTADOS_CHOICES, label='Nuevo Estado')
