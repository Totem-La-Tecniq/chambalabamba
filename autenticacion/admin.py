# apps/autenticacion/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import TipoUsuario, PerfilUsuario

User = get_user_model()


@admin.register(TipoUsuario)
class TipoUsuarioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug", "role_group")
    search_fields = ("nombre", "slug")
    readonly_fields = ("role_group",)  # se crea/sincroniza por signals


class PerfilInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    extra = 0


class UserAdmin(BaseUserAdmin):
    inlines = [PerfilInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
