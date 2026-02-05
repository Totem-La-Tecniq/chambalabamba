from django.urls import path
from . import views


app_name = "visitas"

urlpatterns = [
    path("", views.visitas_index, name="visitas-guiadas"),
    path("<slug:slug>/", views.visita_detail, name="detalle-visitas"),
]
