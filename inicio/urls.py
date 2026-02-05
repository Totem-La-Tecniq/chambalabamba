from django.urls import path
from . import views
from .views import gallery_detail

urlpatterns = [
    path("", views.home, name="home"),
    path("galeria-ultimos-eventos/<slug:slug>/", gallery_detail, name="gallery_detail"),
]
