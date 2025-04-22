from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from .forms import LoginForm
from .oracle_service import validar_usuario_login

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        resultado = validar_usuario_login(data['usuario'], data['clave'])
        if resultado['valido']:
            request.session['usuario'] = data['usuario']
            request.session['id_usuario'] = resultado['id_usuario']
            request.session['rol'] = resultado['rol']
            messages.success(request, f"Bienvenido {data['usuario']} - Rol: {resultado['rol']}")
            return redirect('home')
        else:
            messages.error(request, "Credenciales inválidas o usuario inactivo.")
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('login')
