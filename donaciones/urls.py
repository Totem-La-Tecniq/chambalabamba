from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="donaciones"),
    path("paypal/", views.donacion_paypal, name="donacion_paypal"),
    path("exitosa/", views.donacion_exitosa, name="donacion_exitosa"),
    path("cancelada/", views.donacion_cancelada, name="donacion_cancelada"),
]
