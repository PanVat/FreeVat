import os
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


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
    name = models.CharField(max_length=50, verbose_name=_("Category name"))
    icon = models.FileField(upload_to="models/categories/", null=True, blank=True, verbose_name=_("Category icon"))

    def __str__(self): return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


# Formát
class Format(models.Model):
    name = models.CharField(max_length=20, verbose_name=_("Format name"))
    extension = models.CharField(max_length=10, verbose_name=_("Extension"), default="obj")
    icon = models.FileField(upload_to='models/formats/', verbose_name=_("Format icon"))
    description = models.CharField(max_length=30, verbose_name=_("Description"))

    def __str__(self): return self.name

    class Meta:
        verbose_name = _("Format")
        verbose_name_plural = _("Formats")


# Software
class Software(models.Model):
    name = models.CharField(max_length=20, verbose_name=_("Software name"))
    icon = models.FileField(upload_to='models/software/', verbose_name=_("Format icon"))
    description = models.CharField(max_length=30, verbose_name=_("Software"))

    def __str__(self): return self.name

    class Meta:
        verbose_name = _("Software")
        verbose_name_plural = _("Software")


# 3D model
class Model3D(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=False,
                                 verbose_name=_("Category"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    model = models.FileField(upload_to="models/models/", verbose_name=_("3D model"))
    thumbnail = models.ImageField(upload_to=thumbnail_upload_path, verbose_name=_("Model preview image"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("Creator"))
    uploaded = models.DateTimeField(auto_now_add=True, verbose_name=_("Uploaded at"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Date of last update"))

    def __str__(self): return self.name

    class Meta:
        ordering = ['-uploaded']
        verbose_name = _("3D Model")
        verbose_name_plural = _("3D Models")


# Obrázek do galerie modelů
class ModelImage(models.Model):
    model3d = models.ForeignKey(Model3D, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=gallery_upload_path, verbose_name=_("Gallery Image"))


# Informace o 3D modelu
class Data(models.Model):
    model3d = models.OneToOneField(Model3D, primary_key=True, on_delete=models.CASCADE, verbose_name=_("3D Model"))
    polygons = models.PositiveIntegerField(verbose_name=_("Number of polygons"))
    vertices = models.PositiveIntegerField(verbose_name=_("Number of vertices"))
    file_size = models.PositiveIntegerField(verbose_name=_("File size (bytes)"))
    file_format = models.CharField(max_length=10, verbose_name=_("File format"))


# Uživatelský komentář
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    model3d = models.ForeignKey(Model3D, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(verbose_name=_("Content"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): return f"Comment by {self.user.get_username()} on {self.model3d.name}"
