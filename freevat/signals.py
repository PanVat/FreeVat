from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Model3D, Data
import os


@receiver(post_save, sender=Model3D)
def create_model_data(sender, instance, created, **kwargs):
    if created:
        # Získání přípony (.obj -> obj)
        ext = os.path.splitext(instance.model.name)[1][1:].lower()
        # Získání velikosti v bajtech
        size = instance.model.size

        # Vytvoření záznamu v tabulce Data
        # Polygons a Vertices zatím nastavíme na 0 (vyžadovalo by to 3D knihovnu na analýzu souboru)
        Data.objects.create(
            model3d=instance,
            file_format=ext,
            file_size=size,
            polygons=0,
            vertices=0
        )
