from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout as django_logout
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
            messages.success(request, f"Bienvenido {data['usuario']}")
            return redirect('home')
        else:
            messages.error(request, "Credenciales incorrectas o usuario inactivo.")
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    django_logout(request)
    request.session.flush()
    return redirect('login')
