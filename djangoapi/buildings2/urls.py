from django.urls import path
from . import views

urlpatterns = [
    path("hello_buildings2/", views.HelloBuildings2.as_view(),name="hello_buildings2"),
    path("buildings2_insert/",views.Buildings2Insert.as_view(),name="buildings2_insert"),
    path("buildings2_delete/",views.Buildings2Delete.as_view(),name="buildings2_delete"),
    path('buildings2_view/<str:action>/', views.Buildings2View.as_view(), name='buildings_views'),  # POST requests
    path('buildings2_view/<str:action>/<int:id>/', views.Buildings2View.as_view(), name='buildings_views'),  # POST requests

]