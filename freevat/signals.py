import os
import shutil
import trimesh
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Model3D, Data, ModelImage


# Vytvoří nebo aktualizuje technická data modelu pomocí trimesh
@receiver(post_save, sender=Model3D)
def manage_model_data(sender, instance, created, **kwargs):
    try:
        if instance.model:
            file_path = instance.model.path
            # Získání přípony a velikosti
            ext = os.path.splitext(file_path)[1].lower().replace('.', '')
            f_size = os.path.getsize(file_path)

            # Načtení mesh pro získání polygonů a vrcholů
            mesh = trimesh.load(file_path, force='mesh')

            Data.objects.update_or_create(
                model3d=instance,
                defaults={
                    'polygons': len(mesh.faces),
                    'vertices': len(mesh.vertices),
                    'file_size': f_size,
                    'file_format': ext.upper()
                }
            )
    except Exception as e:
        print(f"Signals Error: Nepodařilo se analyzovat 3D soubor: {e}")


# Smaže 3D model a celou složku s náhledem
@receiver(post_delete, sender=Model3D)
def cleanup_model3d_files(sender, instance, **kwargs):
    # Smazání samotného 3D souboru
    if instance.model and os.path.isfile(instance.model.path):
        os.remove(instance.model.path)

    # Smazání složky s náhledem (thumbnails/jmeno-modelu/)
    if instance.thumbnail:
        thumbnail_dir = os.path.dirname(instance.thumbnail.path)
        if os.path.exists(thumbnail_dir):
            shutil.rmtree(thumbnail_dir)


# Smaže obrázek z galerie a složku, pokud je prázdná
@receiver(post_delete, sender=ModelImage)
def cleanup_gallery_files(sender, instance, **kwargs):
    if instance.image:
        image_path = instance.image.path
        if os.path.isfile(image_path):
            image_dir = os.path.dirname(image_path)
            os.remove(image_path)

            # Pokud ve složce galerie pro tento model nic nezbylo, smažeme ji
            if os.path.exists(image_dir) and not os.listdir(image_dir):
                os.rmdir(image_dir)
