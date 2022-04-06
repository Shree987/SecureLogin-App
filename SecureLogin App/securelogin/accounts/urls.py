from . import views
from django.urls import path

app_name = 'accounts'
urlpatterns = [
    path('', views.home, name="home"),
    path('profile/', views.index, name="index"),

    path('accounts/sign_up/', views.sign_up, name="sign-up"),
    path('accounts/logout/', views.user_logout, name='logout'),
    path('accounts/login/', views.user_login, name='login'),
]