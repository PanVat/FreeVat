import os
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
import trimesh


# =========================================================
# Pomocné funkce pro upload cesty
# =========================================================

def model_folder_name(name: str) -> str:
    """
    model_dog.glb -> model_dog
    My Cool Model -> my-cool-model
    """
    name = os.path.splitext(name)[0]
    return slugify(name)


def thumbnail_upload_path(instance, filename):
    folder = model_folder_name(instance.name)
    return f"models/thumbnails/{folder}/{filename}"


def gallery_upload_path(instance, filename):
    folder = model_folder_name(instance.model3d.name)
    return f"models/gallery/{folder}/{filename}"


# =========================================================
# Kategorie
# =========================================================

class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name=_("Category name")
    )

    icon = models.FileField(
        upload_to="models/categories/",
        null=True,
        blank=True,
        verbose_name=_("Category icon")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


# =========================================================
# Formát 3D modelu
# =========================================================

class Format(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name=_("Format name")
    )

    extension = models.CharField(
        max_length=10,
        verbose_name=_("Extension"),
        default="obj"
    )

    icon = models.FileField(
        upload_to='models/formats/',
        verbose_name=_("Format icon"),
        help_text=_("Upload a small image or SVG representing the format")
    )

    description = models.CharField(
        max_length=30,
        verbose_name=_("Description")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Format")
        verbose_name_plural = _("Formats")


# =========================================================
# Software
# =========================================================

class Software(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name=_("Software name")
    )

    icon = models.FileField(
        upload_to='models/software/',
        verbose_name=_("Format icon"),
        help_text=_("Upload a small image or SVG representing the software")
    )

    description = models.CharField(
        max_length=30,
        verbose_name=_("Software")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Software")
        verbose_name_plural = _("Software")


# =========================================================
# 3D Model
# =========================================================

class Model3D(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name=_("Name")
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name=_("Category")
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
        help_text=_("Enter a short description of the model")
    )

    model = models.FileField(
        upload_to="models/models/",
        verbose_name=_("3D model")
    )

    thumbnail = models.ImageField(
        upload_to=thumbnail_upload_path,
        verbose_name=_("Model preview image")
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Creator")
    )

    uploaded = models.DateTimeField(auto_now_add=True, verbose_name=_("Uploaded at"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Date of last update"))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-uploaded']
        verbose_name = _("3D Model")
        verbose_name_plural = _("3D Models")

    def save(self, *args, **kwargs):
        # 1. Uložíme základní model
        super().save(*args, **kwargs)

        try:
            # 2. Cesta k souboru a přípona
            file_path = self.model.path
            ext = os.path.splitext(file_path)[1].lower().replace('.', '')

            # 3. Analýza souboru
            mesh = trimesh.load(file_path, force='mesh')
            f_size = os.path.getsize(file_path)

            # 4. Zápis do tabulky Data
            Data.objects.update_or_create(
                model3d=self,
                defaults={
                    'polygons': len(mesh.faces),
                    'vertices': len(mesh.vertices),
                    'file_size': f_size,
                    'file_format': ext.upper()
                }
            )
        except Exception as e:
            print(f"Chyba při analýze: {e}")


# =========================================================
# Galerie obrázků
# =========================================================

class ModelImage(models.Model):
    model3d = models.ForeignKey(
        Model3D,
        related_name='images',
        on_delete=models.CASCADE
    )

    # 🔥 ZMĚNA ZDE
    image = models.ImageField(
        upload_to=gallery_upload_path,
        verbose_name=_("Gallery Image")
    )


# =========================================================
# Technická data modelu
# =========================================================

class Data(models.Model):
    model3d = models.OneToOneField(
        Model3D,
        primary_key=True,
        on_delete=models.CASCADE,
        verbose_name=_("3D Model")
    )
    polygons = models.PositiveIntegerField(verbose_name=_("Number of polygons"))
    vertices = models.PositiveIntegerField(verbose_name=_("Number of vertices"))
    file_size = models.PositiveIntegerField(verbose_name=_("File size (bytes)"))
    file_format = models.CharField(max_length=10, verbose_name=_("File format"))


# =========================================================
# Komentáře
# =========================================================

class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Author")
    )

    model3d = models.ForeignKey(
        Model3D,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("3D Model")
    )

    content = models.TextField(
        verbose_name=_("Content"),
        help_text=_("Enter your comment here"),
        error_messages={
            "blank": _("Comment cannot be empty"),
            "max_length": _("Comment cannot exceed 2000 characters")
        }
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at")
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at")
    )

    def __str__(self):
        return f"Comment by {self.user.get_username()} on {self.model3d.name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
