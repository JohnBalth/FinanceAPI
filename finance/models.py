
from django.conf import settings
from django.db import models


class Transaction(models.Model):

    class TransactionType(models.TextChoices):
        INCOME = "INCOME", "Receita"
        EXPENSE = "EXPENSE", "Despesa"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    description = models.CharField(
        max_length=200,
        verbose_name="Descrição",
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Valor",
    )

    transaction_type = models.CharField(
        max_length=7,
        choices=TransactionType.choices,
        verbose_name="Tipo",
    )

    category = models.CharField(
        max_length=100,
        verbose_name="Categoria",
    )

    date = models.DateField(
        verbose_name="Data da transação",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criada em",
    )

    class Meta:
        ordering = ["-date", "-created_at"]
        verbose_name = "Transação"
        verbose_name_plural = "Transações"

    def __str__(self):
        return f"{self.description} - R$ {self.amount}"
