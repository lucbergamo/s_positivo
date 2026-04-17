from django.conf import settings
from django.db import models


class Gasto(models.Model):
    class Classificacao(models.TextChoices):
        ALIMENTACAO = "ALIMENTACAO", "Alimentação"
        TRANSPORTE = "TRANSPORTE", "Transporte"
        MORADIA = "MORADIA", "Moradia"
        SAUDE = "SAUDE", "Saúde"
        LAZER = "LAZER", "Lazer"
        OUTROS = "OUTROS", "Outros"

    # id é criado automaticamente pelo Django (AutoField/BigAutoField)
    criado_em = models.DateTimeField(auto_now_add=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="gastos_criados",
    )

    nome = models.CharField(max_length=120)
    data_gasto = models.DateField()

    classificacao = models.CharField(
        max_length=20,
        choices=Classificacao.choices,
        default=Classificacao.OUTROS,
    )

    valor = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["-data_gasto", "-criado_em"]
        verbose_name = "Gasto"
        verbose_name_plural = "Gastos"

    def __str__(self):
        return f"{self.nome} - {self.valor} ({self.data_gasto})"
    
class Gasto_Fixo(models.Model):
    class Classificacao(models.TextChoices):
        ALIMENTACAO = "ALIMENTACAO", "Alimentação"
        TRANSPORTE = "TRANSPORTE", "Transporte"
        MORADIA = "MORADIA", "Moradia"
        SAUDE = "SAUDE", "Saúde"
        LAZER = "LAZER", "Lazer"
        OUTROS = "OUTROS", "Outros"

    # id é criado automaticamente pelo Django (AutoField/BigAutoField)
    criado_em = models.DateTimeField(auto_now_add=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="gastos_criados_fixos",
    )

    nome = models.CharField(max_length=120)
    data_compensacao = models.PositiveIntegerField(default=0)

    classificacao = models.CharField(
        max_length=20,
        choices=Classificacao.choices,
        default=Classificacao.OUTROS,
    )

    valor_provisonado = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = [ "-criado_em"]
        verbose_name = "Gasto"
        verbose_name_plural = "Gastos"

    def __str__(self):
        return f"{self.nome} - {self.valor} ({self.data_gasto})"
    
class Compromissos(models.Model):
    class Classificacao(models.TextChoices):
        ALIMENTACAO = "ALIMENTACAO", "Alimentação"
        TRANSPORTE = "TRANSPORTE", "Transporte"
        MORADIA = "MORADIA", "Moradia"
        SAUDE = "SAUDE", "Saúde"
        LAZER = "LAZER", "Lazer"
        OUTROS = "OUTROS", "Outros"

    # id é criado automaticamente pelo Django (AutoField/BigAutoField)
    criado_em = models.DateTimeField(auto_now_add=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="compromissos",
    )
    

    nome = models.CharField(max_length=120)
    data_compromisso = models.DateField()

    classificacao = models.CharField(
        max_length=20,
        choices=Classificacao.choices,
        default=Classificacao.OUTROS,
    )

    valor_provisonado = models.DecimalField(max_digits=10, decimal_places=2)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = [ "-criado_em"]
        verbose_name = "Compromisso"
        verbose_name_plural = "Compromissos"

    def __str__(self):
        return f"{self.nome} - {self.valor_pago} ({self.data_compromisso})"