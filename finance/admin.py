
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Transaction

admin.site.unregister(User)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "description",
        "amount",
        "transaction_type",
        "category",
        "date",
        "user",
    )

    list_filter = ("transaction_type", "category", "date")
    search_fields = ("description", "category")


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "is_active",
        "is_staff",
        "date_joined",
        "last_login",
    )

    list_filter = ("is_active", "is_staff", "date_joined")
    search_fields = ("username", "email")
    actions = ["approve_users", "block_users"]

    @admin.action(description="Aprovar usuários selecionados")
    def approve_users(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Bloquear usuários selecionados")
    def block_users(self, request, queryset):
        queryset.filter(is_superuser=False).update(is_active=False)
