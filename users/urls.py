from django.urls import path, include  # new
from . import views

urlpatterns = [
    path('login/', views.login_auth, name='login'),
    path('register/', views.register_request, name='register'),
    path('logout/', views.logout_auth, name='logout'),
    path('change-password/', views.change_password, name='change-password'),
]