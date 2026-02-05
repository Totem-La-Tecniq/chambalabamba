from django.urls import path
from . import views

app_name = "hospedaje"

urlpatterns = [
    path("", views.index, name="index"),
]
