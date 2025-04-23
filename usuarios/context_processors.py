def rol_usuario_context(request):
    return {
        'rol_usuario': request.session.get('rol', None)
    }
