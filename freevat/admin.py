from django.contrib import admin
from .models import Model3D, Data, Comment, Category, ModelImage
from .models import Format, Software

# Registrování modelů v admin rozhraní
admin.site.register(Model3D)
admin.site.register(Data)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(ModelImage)
admin.site.register(Format)
admin.site.register(Software)