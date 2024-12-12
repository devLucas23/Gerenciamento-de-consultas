from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class UserProfileExample(models.Model):

    phone_number = models.CharField(max_length=12)
    address = models.CharField(max_length=150)
    birth_date = models.DateField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


class Medico(models.Model):

    nome = models.CharField(max_length=140)
    crm = models.CharField(max_length=12)
    departamento = models.CharField(max_length=140)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Medico"
        verbose_name_plural = "Medicos"