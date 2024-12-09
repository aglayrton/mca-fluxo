from django.db import models
from django.utils import timezone

class FluxoAgua(models.Model):
    data_hora = models.DateTimeField(default=timezone.now)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.data_hora} - {self.valor} L"


class ConsumoDiario(models.Model):
    data = models.DateField(unique=True)
    consumo_total = models.DecimalField(max_digits=10, decimal_places=2)
    hora = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.data} - {self.consumo_total} L"
