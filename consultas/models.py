from django.db import models

from users.models import Medico


class Consulta(models.Model):
    paciente = models.CharField(max_length=100)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    data_horario = models.DateTimeField()
    especialidade = models.CharField(max_length=100)
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f'Paciente - Médico - Horário[{self.paciente}] -  [{self.medico}] - [{self.data_horario}]'
    
    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
