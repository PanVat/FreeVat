from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns, set_language

urlpatterns = [
    path('i18n/setlang/', set_language, name='set_language'),  # Přepínač jazyka
]

# Vícejazyčné URL (vše, co má být s jazykovým prefixem, sem)
urlpatterns += i18n_patterns(
    path('', include('models.urls')),  # Hlavní stránka
    path('admin/', admin.site.urls),
)

# Rosetta - pro správu překladů
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]