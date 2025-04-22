from django import forms

class LoginForm(forms.Form):
    usuario = forms.CharField(label="Usuario", max_length=100)
    clave = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
