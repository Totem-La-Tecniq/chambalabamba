# apps/autenticacion/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

from django.contrib.auth import get_user_model
from .forms import (
    SignupForm,
    PerfilExternoForm,
    PerfilResidenteForm,
    PerfilRoleForm,
)
from .models import PerfilUsuario

User = get_user_model()


class IngresarView(LoginView):
    template_name = "autenticacion/login.html"
    redirect_authenticated_user = True


class SalirView(LogoutView):
    next_page = reverse_lazy("home")  # ajusta a tu home


def registro(request):
    if request.user.is_authenticated:
        return redirect("perfil")

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Cuenta creada! Ya puedes iniciar sesión.")
            return redirect("login")
    else:
        form = SignupForm()

    return render(request, "autenticacion/registro.html", {"form": form})


@login_required
def perfil(request):
    perfil, _ = PerfilUsuario.objects.get_or_create(user=request.user)
    return render(request, "autenticacion/perfil.html", {"perfil": perfil})


@login_required
def editar_perfil(request):
    perfil = request.user.perfilusuario
    rol_slug = getattr(perfil.tipo_usuario, "slug", "externo")
    FormClass = PerfilResidenteForm if rol_slug == "residente" else PerfilExternoForm

    if request.method == "POST":
        form = FormClass(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado.")
            return redirect("perfil")
    else:
        form = FormClass(instance=perfil)

    return render(
        request,
        "autenticacion/perfil_editar.html",
        {"form": form, "perfil": perfil, "rol": rol_slug},
    )


# ---- Área restringida a residentes (ejemplo) ----------------------------------
def es_residente(u):
    try:
        return u.perfilusuario.es_residente
    except PerfilUsuario.DoesNotExist:
        return False


@login_required
@user_passes_test(es_residente)
def area_residentes(request):
    return render(request, "autenticacion/area_residentes.html")


# ---- Vista Staff para cambiar rol de un usuario -------------------------------
def es_staff(u):
    return u.is_staff


@login_required
@user_passes_test(es_staff)
def cambiar_rol_usuario(request, user_id):
    perfil = get_object_or_404(PerfilUsuario, user_id=user_id)

    if request.method == "POST":
        form = PerfilRoleForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()  # signals sincronizan grupos
            messages.success(request, "Rol actualizado correctamente.")
            return redirect(
                reverse("admin_perfil_detalle", args=[perfil.user_id])
                if "admin_perfil_detalle"
                in [p.name for p in request.resolver_match.namespaces]
                else reverse("perfil")
            )
    else:
        form = PerfilRoleForm(instance=perfil)

    return render(
        request, "autenticacion/cambiar_rol.html", {"form": form, "perfil": perfil}
    )
