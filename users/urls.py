from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),  # Registrace
    path('login/', views.login_view, name='login'),  # Přihlášení
    path('logout/', views.logout_view, name='logout'),  # Odhlášení
]
