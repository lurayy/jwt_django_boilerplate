from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from . import views
urlpatterns = [
    path('auth', obtain_jwt_token),
    path('refresh', refresh_jwt_token),
    path('login', views.user_login, name="somename"),
    path('logout', views.user_logout, name="somename"),
    path('current', views.get_current_user, name="somename"),
]
