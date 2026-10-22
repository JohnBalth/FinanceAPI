
from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "description",
            "amount",
            "transaction_type",
            "category",
            "date",
        ]

        widgets = {
            "description": forms.TextInput(
                attrs={"placeholder": "Ex.: Conta de energia"}
            ),
            "amount": forms.NumberInput(
                attrs={"step": "0.01", "min": "0.01"}
            ),
            "transaction_type": forms.Select(),
            "category": forms.TextInput(
                attrs={"placeholder": "Ex.: Moradia"}
            ),
            "date": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d",
            ),
        }
