from django.db import models
from django.utils import timezone

class Consumo(models.Model):
    data_hora = models.DateTimeField(auto_now_add=True)
    consumo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.data_hora} - {self.consumo} L"

class FluxoAgua(models.Model):
    data_hora = models.DateTimeField(default=timezone.now)
    litros = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=False, blank=False)

    def __str__(self):
        return f"{self.data_hora} - {self.litros} L"


class ConsumoDiarioModel(models.Model):
    data = models.DateField(unique=True)
    consumo_total = models.DecimalField(max_digits=10, decimal_places=2)
    hora = models.TimeField()

    def __str__(self):
        return f"{self.data} - {self.consumo_total} L"
