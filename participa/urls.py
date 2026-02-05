from django.urls import path
from . import views
from .views import estancias_list, estancia_detail

app_name = "participa"
urlpatterns = [
    path("", views.voluntariado, name="voluntariado"),
    path("donaciones/", views.donaciones, name="donaciones"),
    path("estancias", estancias_list, name="estancias"),
    path("estancias/<slug:slug>/", estancia_detail, name="estancia_detail"),
]
