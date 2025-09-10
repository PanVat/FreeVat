from django.db import models

# Jiné tabulky
from .user import User
from .model3d import Model3D

# Třída reprezentující uživatelské recenze k 3D modelům
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    model3d = models.ForeignKey(Model3D, on_delete=models.CASCADE)
    comment = models.TextField(blank=False, null=False, max_length=1000);
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Hvězdičky od 1 do 5
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    class Meta:
        # Uživatel může dát pouze 1 recenzi na 1 model
        unique_together = ('user', 'model3d')
        # Recenze se řadí podle data vytvoření, nejnovější první
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.nickname} - {self.model3d.name} - {self.stars} / 5"