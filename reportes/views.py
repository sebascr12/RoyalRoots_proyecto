from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def reportes_view(request):
    if request.session.get("rol") == "ADMIN":
        return render(request, 'reportes.html')
    return render(request, 'error.html', {"mensaje": "Acceso restringido a administradores."})