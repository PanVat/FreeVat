from . import views
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns, set_language

urlpatterns = [
    # Přepínač jazyka
    path('i18n/setlang/', set_language, name='set_language'),
    # Účty přes Allauth
    path('accounts/', include('allauth.urls')),
]

# Vícejazyčné URL (vše, co má být s jazykovým prefixem, sem)
urlpatterns += i18n_patterns(
    path('', views.index, name='index'),  # Hlavní stránka
    path('admin/', admin.site.urls),
    # Přesměrování do aplikace 'users'
    path('users/', include('users.urls')),
    # Nahrání 3D modelu
    path('upload/', views.upload_model, name='upload'),
    # Uživatelský profil
    path('profile/', views.user_profile, name='profile'),
    # Nahrání 3D modelu
    path('upload/', views.upload_model, name='upload')
)

# Rosetta - pro správu překladů
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
