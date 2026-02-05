from django.urls import path
from . import views


app_name = "proyectos"
urlpatterns = [
    path("", views.index, name="proyectos"),
]
