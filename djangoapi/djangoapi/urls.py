"""
URL configuration for djangoapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required

from rest_framework import permissions

#from drf_yasg.views import get_schema_view
#from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from core.views import custom_logout_view

urlpatterns = [
    # Sirve la UI de Swagger/Redoc
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Genera el archivo schema/openapi (requerido para la UI)
    path('docs/schema/', SpectacularAPIView.as_view(), name='schema'),

    path('admin/', admin.site.urls),
    path("accounts/logout/", custom_logout_view, name="logout"),
    path("accounts/", include("django.contrib.auth.urls")),

    path('codelist/', include('codelist.urls')),
    path('core/', include('core.urls')),
    path('buildings/', include('buildings.urls')),
    path('flowers/', include('flowers.urls')),
    path('accidentes/', include('accidentes.urls')),
    path('buildings2/', include('buildings2.urls')),
    path("campus/", include("campus.urls")),
]
