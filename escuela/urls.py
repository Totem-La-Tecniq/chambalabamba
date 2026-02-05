from django.urls import path
from . import views

app_name = "escuela"

urlpatterns = [
    path("", views.index, name="index"),
]
