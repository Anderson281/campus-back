from django.urls import path, include
from . import views, viewsKnoxLoginManagenent
from rest_framework import routers

router = routers.DefaultRouter()
#router.register(r'core', viewsKnoxLoginManagenent.KnoxLoginView)

urlpatterns = [
    path("hello_world/", views.HelloWord.as_view(),name="hello_world"),
    path('', include(router.urls)),
    path('not_loggedin/', views.notLoggedIn, name="not_loggedin"),
    path('login/', views.LoginView.as_view(),name="core_login"),
    path('logout/', views.LogoutView.as_view(),name="core_logout"),

    #knox operations with token authentication in the header
    #key: Authorization
    #Value: Token the_token
    path('isloggedin/', views.IsLoggedIn.as_view(),name="isloggedin"),
    path('knox_login/', viewsKnoxLoginManagenent.KnoxLogin.as_view(), name='knox_login'),
    path('knox_logout/', viewsKnoxLoginManagenent.KnoxLogout.as_view(), name='knox_logout'),
    path('is_valid_token/', viewsKnoxLoginManagenent.IsValidToken.as_view(), name='is_valid_token'),
    path('logout_all_user_sessions/', viewsKnoxLoginManagenent.LogoutAllUserSessionsView.as_view(), name='logout_all_user_sessions'),
    path('logout_all_users_sessions/', viewsKnoxLoginManagenent.LogoutAllUsersSessionsView.as_view(), name='logout_all_users_sessionst'),
]