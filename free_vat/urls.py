from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('models.urls')), # Hlavní stránka 'index.html'
    path('admin/', admin.site.urls),
]
