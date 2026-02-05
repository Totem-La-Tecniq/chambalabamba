# apps/autenticacion/urls.py
from django.urls import path
from .views import (
    IngresarView,
    SalirView,
    registro,
    perfil,
    editar_perfil,
    area_residentes,
)

urlpatterns = [
    path("login/", IngresarView.as_view(), name="login"),
    path("logout/", SalirView.as_view(), name="logout"),
    path("registro/", registro, name="registro"),
    path("perfil/", perfil, name="perfil"),
    path("perfil/editar/", editar_perfil, name="perfil_editar"),
    path("residentes/", area_residentes, name="area_residentes"),
    # path("cambiar-rol/<int:user_id>/", cambiar_rol_usuario, name="cambiar_rol_usuario"),
]
