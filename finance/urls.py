
from django.urls import path
from .views import (
    TransactionListCreateView,
    TransactionDetailView,
    transaction_form,
    dashboard,
    edit_transaction,
    register
)

urlpatterns = [
    path(
        "transactions/",
        TransactionListCreateView.as_view(),
        name="transaction-list-create",
    ),
    path(
        "transactions/<int:pk>/",
        TransactionDetailView.as_view(),
        name="transaction-detail",
    ),
    path(
        "nova-transacao/",
        transaction_form,
        name="transaction-form",
    ),
    path(
        "dashboard/",
        dashboard,
        name="dashboard",
    ),
    path(
        "transactions/<int:pk>/editar/",
        edit_transaction,
        name="edit-transaction",
    ),
    path(
    "cadastro/",
    register,
    name="register",
    ),
]
