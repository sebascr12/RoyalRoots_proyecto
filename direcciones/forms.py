from django import forms
from direcciones.oracle_service import (
    obtener_provincias_disponibles,
    obtener_cantones_disponibles,
    obtener_distritos_disponibles,
    obtener_estados_disponibles
)

class ProvinciaForm(forms.Form):
    provincia = forms.CharField(label='Provincia', max_length=100)
    estado = forms.ChoiceField(
        choices=[('ACTIVO', 'ACTIVO'), ('INACTIVO', 'INACTIVO')],
        label='Estado'
    )

    def clean_provincia(self):
        return self.cleaned_data['provincia'].upper()

    def clean_estado(self):
        return self.cleaned_data['estado'].upper()


class ActualizarProvinciaForm(forms.Form):
    nuevo_nombre = forms.CharField(label="Nuevo nombre de la provincia", max_length=100)
    estado = forms.ChoiceField(
        choices=[('ACTIVO', 'ACTIVO'), ('INACTIVO', 'INACTIVO')],
        label="Estado"
    )

    def clean_nuevo_nombre(self):
        return self.cleaned_data['nuevo_nombre'].upper()

    def clean_estado(self):
        return self.cleaned_data['estado'].upper()


class CantonForm(forms.Form):
    canton = forms.CharField(label='Nombre del Cantón', max_length=100)
    provincia = forms.CharField(label='Provincia (nombre)', max_length=100)
    estado = forms.ChoiceField(
        label='Estado',
        choices=[('ACTIVO', 'ACTIVO'), ('INACTIVO', 'INACTIVO')]
    )

    def clean_canton(self):
        return self.cleaned_data['canton'].upper()

    def clean_provincia(self):
        return self.cleaned_data['provincia'].upper()

    def clean_estado(self):
        return self.cleaned_data['estado'].upper()


class ActualizarCantonForm(forms.Form):
    nuevo_nombre = forms.CharField(label='Nuevo Nombre del Cantón', max_length=100)
    provincia = forms.CharField(label='Provincia (nombre)', max_length=100)
    estado = forms.ChoiceField(
        label='Estado',
        choices=[('ACTIVO', 'ACTIVO'), ('INACTIVO', 'INACTIVO')]
    )

    def clean_nuevo_nombre(self):
        return self.cleaned_data['nuevo_nombre'].upper()

    def clean_provincia(self):
        return self.cleaned_data['provincia'].upper()

    def clean_estado(self):
        return self.cleaned_data['estado'].upper()


class DistritoForm(forms.Form):
    distrito = forms.CharField(label='Nombre del Distrito', max_length=100)
    canton = forms.CharField(label='Cantón', max_length=100)
    estado = forms.CharField(label='Estado', max_length=100)

    def clean_distrito(self):
        return self.cleaned_data['distrito'].upper()

    def clean_canton(self):
        return self.cleaned_data['canton'].upper()

    def clean_estado(self):
        return self.cleaned_data['estado'].upper()


class ActualizarDistritoForm(forms.Form):
    nuevo_nombre = forms.CharField(label='Nuevo Nombre del Distrito', max_length=100)
    canton = forms.CharField(label='Nuevo Cantón', max_length=100)
    estado = forms.CharField(label='Nuevo Estado', max_length=100)

    def clean_nuevo_nombre(self):
        return self.cleaned_data['nuevo_nombre'].upper()

    def clean_canton(self):
        return self.cleaned_data['canton'].upper()

    def clean_estado(self):
        return self.cleaned_data['estado'].upper()


class DireccionForm(forms.Form):
    provincia = forms.ChoiceField(label='Provincia', required=True)
    canton = forms.ChoiceField(label='Cantón', required=True)
    distrito = forms.ChoiceField(label='Distrito', required=True)
    estado = forms.ChoiceField(label='Estado', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['provincia'].choices = [(p.upper(), p.upper()) for p in obtener_provincias_disponibles()]
        self.fields['canton'].choices = [(c.upper(), c.upper()) for c in obtener_cantones_disponibles()]
        self.fields['distrito'].choices = [(d.upper(), d.upper()) for d in obtener_distritos_disponibles()]
        self.fields['estado'].choices = [(e.upper(), e.upper()) for e in obtener_estados_disponibles()]


class ActualizarDireccionForm(forms.Form):
    nueva_provincia = forms.ChoiceField(label='Provincia', required=True)
    nuevo_canton = forms.ChoiceField(label='Cantón', required=True)
    nuevo_distrito = forms.ChoiceField(label='Distrito', required=True)
    nuevo_estado = forms.ChoiceField(label='Estado', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nueva_provincia'].choices = [(p.upper(), p.upper()) for p in obtener_provincias_disponibles()]
        self.fields['nuevo_canton'].choices = [(c.upper(), c.upper()) for c in obtener_cantones_disponibles()]
        self.fields['nuevo_distrito'].choices = [(d.upper(), d.upper()) for d in obtener_distritos_disponibles()]
        self.fields['nuevo_estado'].choices = [(e.upper(), e.upper()) for e in obtener_estados_disponibles()]
