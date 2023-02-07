from django.db import models
from django.contrib.auth.models import User

# crea los modelos para la base de datos para crear tablas en sql
class Task(models.Model):
    
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    #mostrar el detalle en pestaña admin
    def __str__(self):
        return self.title + ' - ' + self.user.username
    
