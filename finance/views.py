from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema,
    extend_schema_view,
)
from rest_framework import generics, permissions
from .forms import TransactionForm
from .models import Transaction
from .serializers import (
    TransactionSerializer,
    ValidationErrorSerializer,
)


# ==========================================================
# EXEMPLOS DA DOCUMENTAÇÃO SWAGGER
# ==========================================================

TRANSACTION_REQUEST_EXAMPLE = OpenApiExample(
    name="Exemplo de criação de despesa",
    value={
        "description": "Compra no supermercado",
        "amount": "150.00",
        "transaction_type": "EXPENSE",
        "category": "Alimentação",
        "date": "2026-10-19",
    },
    request_only=True,
)

TRANSACTION_RESPONSE_EXAMPLE = OpenApiExample(
    name="Transação criada com sucesso",
    value={
        "id": 11,
        "description": "Compra no supermercado",
        "amount": "150.00",
        "transaction_type": "EXPENSE",
        "category": "Alimentação",
        "date": "2026-10-19",
        "created_at": "2026-10-19T12:00:00Z",
        "user": 1,
    },
    response_only=True,
    status_codes=["201"],
)

INVALID_AMOUNT_EXAMPLE = OpenApiExample(
    name="Erro: valor inválido",
    value={
        "amount": [
            "O valor da transação deve ser maior que zero."
        ]
    },
    response_only=True,
    status_codes=["400"],
)

INVALID_DESCRIPTION_EXAMPLE = OpenApiExample(
    name="Erro: descrição em branco",
    value={
        "description": [
            "Este campo pode não estar em branco."
        ]
    },
    response_only=True,
    status_codes=["400"],
)

INVALID_CATEGORY_EXAMPLE = OpenApiExample(
    name="Erro: categoria em branco",
    value={
        "category": [
            "Este campo pode não estar em branco."
        ]
    },
    response_only=True,
    status_codes=["400"],
)


# ==========================================================
# API REST: LISTAR E CRIAR TRANSAÇÕES
# ==========================================================

@extend_schema_view(
    get=extend_schema(
        summary="Listar transações",
        description=(
            "Retorna uma lista de transações do usuário autenticado. "
            "Cada usuário acessa somente suas próprias transações."
        ),
        tags=["Transações"],
        responses={
            200: TransactionSerializer(many=True),
        },
        examples=[
            OpenApiExample(
                name="Exemplo de transação na lista",
                value={
                    "id": 11,
                    "description": "Salário",
                    "amount": "3250.00",
                    "transaction_type": "INCOME",
                    "category": "Salário",
                    "date": "2026-10-05",
                    "created_at": "2026-10-05T12:00:00Z",
                    "user": 1,
                },
                response_only=True,
                status_codes=["200"],
            ),
        ],
    ),
    post=extend_schema(
        summary="Criar transação",
        description=(
            "Cadastra uma nova receita ou despesa para o usuário "
            "autenticado. O usuário é definido automaticamente. "
            "O valor deve ser maior que zero e a descrição e a "
            "categoria não podem ficar vazias."
        ),
        tags=["Transações"],
        request=TransactionSerializer,
        responses={
            201: TransactionSerializer,
            400: ValidationErrorSerializer,
        },
        examples=[
            TRANSACTION_REQUEST_EXAMPLE,
            TRANSACTION_RESPONSE_EXAMPLE,
            INVALID_AMOUNT_EXAMPLE,
            INVALID_DESCRIPTION_EXAMPLE,
            INVALID_CATEGORY_EXAMPLE,
        ],
    ),
)
class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ==========================================================
# API REST: CONSULTAR, EDITAR E EXCLUIR UMA TRANSAÇÃO
# ==========================================================

@extend_schema_view(
    get=extend_schema(
        summary="Consultar transação",
        description=(
            "Retorna os detalhes de uma transação pertencente "
            "ao usuário autenticado. Se a transação não existir "
            "ou pertencer a outro usuário, retorna 404."
        ),
        tags=["Transações"],
        responses={
            200: TransactionSerializer,
            404: None,
        },
        examples=[
            OpenApiExample(
                name="Transação consultada",
                value={
                    "id": 11,
                    "description": "Compra no supermercado",
                    "amount": "150.00",
                    "transaction_type": "EXPENSE",
                    "category": "Alimentação",
                    "date": "2026-10-19",
                    "created_at": "2026-10-19T12:00:00Z",
                    "user": 1,
                },
                response_only=True,
                status_codes=["200"],
            ),
        ],
    ),
    put=extend_schema(
        summary="Atualizar transação",
        description=(
            "Atualiza uma transação existente. Envie todos os "
            "campos obrigatórios aceitos pelo serializer. "
            "Somente o proprietário da transação pode atualizá-la."
        ),
        tags=["Transações"],
        request=TransactionSerializer,
        responses={
            200: TransactionSerializer,
            400: ValidationErrorSerializer,
            404: None,
        },
        examples=[
            OpenApiExample(
                name="Exemplo de atualização completa",
                value={
                    "description": "Compra semanal",
                    "amount": "180.00",
                    "transaction_type": "EXPENSE",
                    "category": "Alimentação",
                    "date": "2026-10-19",
                },
                request_only=True,
            ),
            OpenApiExample(
                name="Erro: valor inválido",
                value={
                    "amount": [
                        "O valor da transação deve ser maior que zero."
                    ]
                },
                response_only=True,
                status_codes=["400"],
            ),
        ],
    ),
    patch=extend_schema(
        summary="Atualizar parcialmente uma transação",
        description=(
            "Atualiza somente os campos enviados para uma transação "
            "pertencente ao usuário autenticado."
        ),
        tags=["Transações"],
        responses={
            200: TransactionSerializer,
            400: ValidationErrorSerializer,
            404: None,
        },
        examples=[
            OpenApiExample(
                name="Exemplo de atualização parcial",
                value={
                    "amount": "175.00",
                },
                request_only=True,
            ),
            OpenApiExample(
                name="Erro: valor inválido",
                value={
                    "amount": [
                        "O valor da transação deve ser maior que zero."
                    ]
                },
                response_only=True,
                status_codes=["400"],
            ),
        ],
    ),
    delete=extend_schema(
        summary="Excluir transação",
        description=(
            "Exclui uma transação pertencente ao usuário "
            "autenticado. A operação não pode ser desfeita."
        ),
        tags=["Transações"],
        responses={
            204: None,
            404: None,
        },
    ),
)
class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


# ==========================================================
# FORMULÁRIO DE TRANSAÇÃO
# ==========================================================

@login_required
def transaction_form(request):
    return render(
        request,
        "finance/transaction_form.html",
    )


# ==========================================================
# DASHBOARD FINANCEIRO
# ==========================================================

@login_required
def dashboard(request):
    # Somente as transações do usuário autenticado
    user_transactions = Transaction.objects.filter(user=request.user)

    current_year = timezone.localdate().year

    selected_month = request.GET.get("mes", "").strip()
    selected_year = request.GET.get("ano", str(current_year)).strip()

    # Validar mês
    if selected_month.isdigit() and 1 <= int(selected_month) <= 12:
        month_number = int(selected_month)
    else:
        selected_month = ""
        month_number = None

    # Validar ano
    if selected_year.isdigit() and 1900 <= int(selected_year) <= 2100:
        year_number = int(selected_year)
    else:
        selected_year = str(current_year)
        year_number = current_year

    # Anos disponíveis para o filtro
    available_years = {
        item.year
        for item in user_transactions.dates(
            "date",
            "year",
            order="DESC",
        )
    }
    available_years.add(current_year)
    available_years.add(year_number)
    available_years = sorted(available_years, reverse=True)

    # Filtrar por ano e, opcionalmente, por mês
    period_transactions = user_transactions.filter(
        date__year=year_number
    )

    if month_number is not None:
        period_transactions = period_transactions.filter(
            date__month=month_number
        )

    # Calcular receitas e despesas
    totals = period_transactions.aggregate(
        income=Sum(
            "amount",
            filter=Q(
                transaction_type=Transaction.TransactionType.INCOME
            ),
        ),
        expenses=Sum(
            "amount",
            filter=Q(
                transaction_type=Transaction.TransactionType.EXPENSE
            ),
        ),
    )

    income = totals["income"] or Decimal("0.00")
    expenses = totals["expenses"] or Decimal("0.00")
    balance = income - expenses

    # Dados utilizados pelo gráfico
    chart_data = {
        "income": float(income),
        "expenses": float(expenses),
    }

    # Busca por descrição ou categoria
    search_query = request.GET.get("q", "").strip()

    # Filtro por tipo de transação
    selected_type = request.GET.get("tipo", "").strip()

    transactions = period_transactions

    if search_query:
        transactions = transactions.filter(
            Q(description__icontains=search_query)
            | Q(category__icontains=search_query)
        )

    if selected_type in (
        Transaction.TransactionType.INCOME,
        Transaction.TransactionType.EXPENSE,
    ):
        transactions = transactions.filter(
            transaction_type=selected_type
        )
    else:
        selected_type = ""

    context = {
        "income": income,
        "expenses": expenses,
        "balance": balance,
        "transactions": transactions[:10],
        "search_query": search_query,
        "selected_type": selected_type,
        "selected_month": selected_month,
        "selected_year": selected_year,
        "available_years": available_years,
        "chart_data": chart_data,
    }

    return render(
        request,
        "finance/dashboard.html",
        context,
    )


# ==========================================================
# EDITAR UMA TRANSAÇÃO PELO DASHBOARD
# ==========================================================

@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(
        Transaction,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":
        form = TransactionForm(
            request.POST,
            instance=transaction,
        )

        if form.is_valid():
            form.save()
            return redirect("/api/dashboard/")
    else:
        form = TransactionForm(instance=transaction)

    return render(
        request,
        "finance/edit_transaction.html",
        {
            "form": form,
            "transaction": transaction,
        },
    )


# ==========================================================
# CADASTRO DE USUÁRIOS
# ==========================================================


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # A conta começa bloqueada até a aprovação do administrador.
            user.is_active = False
            user.save()

            return render(
                request,
                "registration/register_pending.html",
                {"username": user.username},
            )
    else:
        form = UserCreationForm()

    return render(
        request,
        "registration/register.html",
        {"form": form},
    )
