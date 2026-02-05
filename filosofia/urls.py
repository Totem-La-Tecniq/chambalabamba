from django.urls import path
from . import views

app_name = "filosofia"

urlpatterns = [
    path("", views.index, name="index"),
]
