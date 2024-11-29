from django.db import models

class Consumo(models.Model):
    data_hora = models.DateTimeField(auto_now_add=True)
    consumo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.data_hora} - {self.consumo} L"

class FluxoAgua(models.Model):
    data = models.DateField(verbose_name='Data', unique=True)
    consumo_diario = models.DecimalField(verbose_name='Consumo Diário', max_digits=10, decimal_places=2)
    hora = models.TimeField(verbose_name='Hora', default='00:00')

    def __str__(self):
        return f"{self.data} - {self.hora} - {self.consumo_diario} L"
