from . import views
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns, set_language
from django.conf.urls.static import static  # Pro statické soubory

urlpatterns = [
    # Přepínač jazyka
    path('i18n/setlang/', set_language, name='set_language'),
    # Účty přes Allauth
    path('accounts/', include('allauth.urls')),
]

# Vícejazyčné URL
urlpatterns += i18n_patterns(
    # Hlavní stránka
    path('', views.index, name='index'),
    # Administrační rozhraní
    path('admin/', admin.site.urls),
    # Uživatelské URL
    path('users/', include('users.urls')),
    # Nahrávání modelů
    path('upload/', views.upload_model, name='upload'),
    # Profil uživatele
    path('profile/', views.user_profile, name='profile'),
    # Cesta pro seznam modelů
    path('models/', views.model_list, name='model_list'),
    # Zobrazení všech modelů v dané kategorii
    path('models/category/<str:category_name>/', views.model_list, name='model_list_by_category'),
    # Zobrazení modelů v daném formátu
    path('models/format/<str:format_ext>/', views.model_list, name='model_list_by_format'),
    path('models/software/<str:software_name>/', views.model_list, name='model_list_by_software'),
    # PŘIDEJ TENTO ŘÁDEK:
    path('model/<int:pk>/', views.model_detail, name='model_detail'),
)

# Rosetta
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]

# Konfigurace pro vývoj (DEBUG mode)
if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
# Django bude servírovat nahrané soubory (modely, obrázky) z /media/
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
