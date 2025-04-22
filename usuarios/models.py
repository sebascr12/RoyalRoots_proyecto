from django.db import models

class Usuario(models.Model):
    id_usuario = models.IntegerField(primary_key=True)
    usuario = models.CharField(max_length=100)
    clave = models.CharField(max_length=100)
    id_rol = models.IntegerField()
    id_estado = models.IntegerField()

    def __str__(self):
        return self.usuario
