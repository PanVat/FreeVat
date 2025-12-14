from . import views
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns, set_language
# DŮLEŽITÉ: Import pro statické soubory
from django.conf.urls.static import static

urlpatterns = [
    # Přepínač jazyka
    path('i18n/setlang/', set_language, name='set_language'),
    # Účty přes Allauth
    path('accounts/', include('allauth.urls')),
]

# Vícejazyčné URL
urlpatterns += i18n_patterns(
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('upload/', views.upload_model, name='upload'),  # Byla tu duplicita, smazal jsem ji
    path('profile/', views.user_profile, name='profile'),
)

# Rosetta
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]

# DŮLEŽITÉ: Konfigurace pro vývoj (DEBUG mode)
if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
    # Toto zajistí, že Django bude servírovat nahrané soubory (modely, obrázky) z /media/
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
