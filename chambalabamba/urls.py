"""
URL configuration for chambalabamba project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from it my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based viewsgit
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("inicio.urls")),
    path("contacto/", include("contacto.urls")),
    path("nosotros/", include(("nosotros.urls", "nosotros"), namespace="nosotros")),
    path("eventos/", include("eventos.urls")),
    path("blog/", include("blog.urls")),
    path("participa/", include("participa.urls")),
    path("visitas/", include("visitas.urls", "visitas")),
    path("donaciones/", include("donaciones.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("tienda/", include("tienda.urls")),
    path("auth/", include("autenticacion.urls")),
    path("proyectos/", include("proyectos.urls")),
    path("cooperaciones/", include(("cooperaciones.urls", "coops"), namespace="coops")),
    # path('login/', auth_views.LoginView.as_view(template_name='autenticacion/login.html'), name='login'),
]
"""
# PROD (Render): si optaste por servir media con Django (no CDN), deja este fallback:
if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]


# DEV: sirve media automáticamente si DEBUG=True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
# En dev (DEBUG=True): usa helper estándar esto para withenoise configuracion para storage en render disco montado 1GB
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # En producción: servir media con Django
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    ]
