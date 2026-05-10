from django.urls import path, include
from . import views

urlpatterns = [
    path("hello_world/", views.HelloWord.as_view(),name="hello_world"),
    path("get_flower_by_id/", views.Flower2.as_view(),name="get_flower_by_id"),
    path("insert_flower/", views.Flower2.as_view(),name="insert_flower"),

    #post: insert
    #get: selectall
    path('flowers/<str:action>/', views.Flower.as_view(), name='buildings_views'),  # POST requests
    
    #get: selectone/id/
    #post: delete/id/, update/id/
    path('flowers/<str:action>/<int:id>/', views.Flower.as_view(), name='buildings_views'),  # POST requests
]