# campus/urls.py
# Rutas propias de la app campus.
# Django entrara aqui desde djangoapi/urls.py cuando la URL empiece por /campus/.

from django.urls import path
from . import views

urlpatterns = [
    path("hello_world/", views.HelloWorld.as_view(), name="hello_world"),
    path("hello/", views.HelloCampus.as_view(), name="hello_campus"),
    path("<str:tabla>/<str:accion>/", views.CampusView.as_view(), name="campus_accion"),
    path("<str:tabla>/<str:accion>/<int:id>/", views.CampusView.as_view(), name="campus_accion_id"),
]
