from django.db import models

# Jiné tabulky
from property import Property
from user import User

# Třída reprezentující 3D modely
class Model3D(models.Model):
    name = models.CharField(max_length=64)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    property= models.ForeignKey(Property, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
