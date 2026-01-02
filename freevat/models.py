import os
from django.conf import settings
from django.db import models
from django.utils.text import slugify

# Funkce pro nastavení složek, které se dynamicky vytvoří při nahrání modelu
def model_folder_name(name: str) -> str:
    name = os.path.splitext(name)[0]
    return slugify(name)


def thumbnail_upload_path(instance, filename):
    folder = model_folder_name(instance.name)
    return f"models/thumbnails/{folder}/{filename}"


def gallery_upload_path(instance, filename):
    folder = model_folder_name(instance.model3d.name)
    return f"models/gallery/{folder}/{filename}"


# Kategorie
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Category name")
    icon = models.FileField(upload_to="models/categories/", null=True, blank=True, verbose_name="Category icon")

    def __str__(self): return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


# Formát
class Format(models.Model):
    name = models.CharField(max_length=20, verbose_name="Format name")
    extension = models.CharField(max_length=10, verbose_name="Extension", default="obj")
    icon = models.FileField(upload_to='models/formats/', verbose_name="Format icon")
    description = models.CharField(max_length=30, verbose_name="Description")

    def __str__(self): return self.name

    class Meta:
        verbose_name = "Format"
        verbose_name_plural = "Formats"


# Software
class Software(models.Model):
    name = models.CharField(max_length=20, verbose_name="Software name")
    icon = models.FileField(upload_to='models/software/', verbose_name="Software icon")
    description = models.CharField(max_length=30, verbose_name="Software")

    def __str__(self): return self.name

    class Meta:
        verbose_name = "Software"
        verbose_name_plural = "Software"


# 3D model
class Model3D(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=False,
                                 verbose_name="Category")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    model = models.FileField(upload_to="models/models/", verbose_name="3D model")
    thumbnail = models.ImageField(upload_to=thumbnail_upload_path, verbose_name="Model preview image")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Creator")
    uploaded = models.DateTimeField(auto_now_add=True, verbose_name="Uploaded at")
    updated = models.DateTimeField(auto_now=True, verbose_name="Date of last update")

    def __str__(self): return self.name

    class Meta:
        ordering = ['-uploaded']
        verbose_name = "3D Model"
        verbose_name_plural = "3D Models"


# Obrázek do galerie modelů
class ModelImage(models.Model):
    model3d = models.ForeignKey(Model3D, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=gallery_upload_path, verbose_name="Gallery Image")


# Informace o 3D modelu
class Data(models.Model):
    model3d = models.OneToOneField(Model3D, primary_key=True, on_delete=models.CASCADE, verbose_name="3D Model")
    polygons = models.PositiveIntegerField(verbose_name="Number of polygons")
    vertices = models.PositiveIntegerField(verbose_name="Number of vertices")
    file_size = models.PositiveIntegerField(verbose_name="File size (bytes)")
    file_format = models.CharField(max_length=10, verbose_name="File format")


# Uživatelský komentář
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    model3d = models.ForeignKey(Model3D, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(verbose_name="Content")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): return f"Comment by {self.user.get_username()} on {self.model3d.name}"
