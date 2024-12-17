from django.db import models

from users.models import Medico


class Consulta(models.Model):
    paciente = models.CharField(max_length=100)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    data_horario = models.DateTimeField()
    especialidade = models.CharField(max_length=100)
    observacoes = models.TextField(blank=True)

    def __str__(self):
        ret_def = 'Paciente - Médico - Horário'
        ret_def2 = f'{self.paciente}] - [{self.medico}] - [{self.data_horario}'
        return f'{ret_def}{ret_def2}'
       
    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
