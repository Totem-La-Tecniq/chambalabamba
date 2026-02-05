from django.urls import path
from . import views

app_name = "voluntariado"

urlpatterns = [
    path("", views.index, name="index"),
]
