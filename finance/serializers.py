from decimal import Decimal
from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.01"),
        help_text="Valor da transação. Deve ser maior que zero.",
    )

    description = serializers.CharField(
        max_length=200,
        allow_blank=False,
        trim_whitespace=True,
        help_text="Descrição da receita ou despesa.",
    )

    category = serializers.CharField(
        max_length=100,
        allow_blank=False,
        trim_whitespace=True,
        help_text="Categoria da transação.",
    )

    class Meta:
        model = Transaction
        fields = [
            "id",
            "description",
            "amount",
            "transaction_type",
            "category",
            "date",
            "created_at",
            "user",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "user",
        ]

    def validate_amount(self, value):
        if value <= Decimal("0.00"):
            raise serializers.ValidationError(
                "O valor da transação deve ser maior que zero."
            )

        return value

    def validate_description(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "A descrição não pode ficar vazia."
            )

        return value

    def validate_category(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "A categoria não pode ficar vazia."
            )

        return value


class ValidationErrorSerializer(serializers.Serializer):
    """
    Representa a estrutura de uma resposta de erro de validação.
    """

    detail = serializers.CharField(
        required=False,
        help_text="Mensagem geral do erro, quando aplicável.",
    )

    description = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="Erros de validação da descrição.",
    )

    amount = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="Erros de validação do valor.",
    )

    transaction_type = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="Erros de validação do tipo de transação.",
    )

    category = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="Erros de validação da categoria.",
    )

    date = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="Erros de validação da data.",
    )
