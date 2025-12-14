from django.contrib import admin
from .models import Model3D, Data, Comment

# Registrování modelů v admin rozhraní
admin.site.register(Model3D)
admin.site.register(Data)
admin.site.register(Comment)