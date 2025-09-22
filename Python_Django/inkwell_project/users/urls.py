from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_create, name='user_create'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('me/', views.current_user, name='current_user'),
]