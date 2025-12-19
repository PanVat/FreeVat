from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Registrace uživatele (vytvoření nového účtu)
    path('register/', views.register_view, name='register'),
    # Přihlášení uživatele k existujícímu účtu nebo přes OAuth
    path('login/', views.login_view, name='login'),
    # Odhlášení přihlášeného uživatele
    path('logout/', views.logout_view, name='logout'),
    # Úprava údajů o uživateli
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    # Změna uživatelského hesla
    path('profile/password/', views.change_password, name='change_password'),
]
