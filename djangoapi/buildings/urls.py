from django.urls import path, include
from . import views
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'buildings', views.BuildingsModelViewSet)
router.register(r'owners', views.OwnersModelViewSet)
router.register(r'buildingsowners', views.BuildingsOwnersModelViewSet)


urlpatterns = [
    path("hello_world/", views.HelloWord.as_view(),name="hello_world"),
    path('', include(router.urls)),
    path('buildings_view/<str:action>/', views.BuildigsView.as_view(), name='buildings_views'),  # POST requests
    path('buildings_view/<str:action>/<int:id>/', views.BuildigsView.as_view(), name='buildings_views'),  # POST requests
]