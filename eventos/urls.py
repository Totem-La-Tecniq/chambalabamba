from django.urls import path
from . import views

app_name = "eventos"

urlpatterns = [
    path("escuela-viva/", views.escuela_viva, name="escuela_viva"),
    path("talleres/", views.talleres, name="talleres"),
    path("talleres/<slug:slug>/", views.taller_detail, name="taller_detail"),
    path("retiros/", views.retiros, name="retiros"),
    path("artes/", views.artes, name="artes"),
    path("terapias/", views.terapias, name="terapias"),
    path("festivales/", views.festivales, name="festivales"),
    path("festivales/<slug:slug>/", views.festival_detail, name="festival_detail"),
]
