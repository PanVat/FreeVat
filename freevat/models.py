from django.conf import settings
from django.db import models

# Pro překlad textů
from django.utils.translation import gettext_lazy as _


# Kategorie pro 3D modely (např. Architektura, Postavy, Auta...)
class Category(models.Model):
    # Název kategorie
    name = models.CharField(max_length=50, verbose_name=_("Category name"))

    # Ikonka kategorie
    icon = models.FileField(upload_to="models/categories",
                            null=True,
                            blank=True,
                            verbose_name=_("Category icon"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


# Formát 3D modelu
class Format(models.Model):
    # Název formátu
    name = models.CharField(max_length=20, verbose_name=_("Format name"))

    # Přípona
    extension = models.CharField(max_length=10, verbose_name=_("Extension"), default="obj")

    # Ikona formátu
    icon = models.FileField(
        upload_to='models/formats/',
        verbose_name=_("Format icon"),
        help_text=_("Upload a small image or SVG representing the format")
    )

    # Jednoduchý popisek (např. ".max, .3ds, .obj")
    description = models.CharField(max_length=30, verbose_name=_("Description"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Format")
        verbose_name_plural = _("Formats")

# Formát 3D software
class Software(models.Model):
    # Název formátu
    name = models.CharField(max_length=20, verbose_name=_("Software name"))

    # Ikona formátu
    icon = models.FileField(
        upload_to='models/software/',
        verbose_name=_("Format icon"),
        help_text=_("Upload a small image or SVG representing the software")
    )

    # Jednoduchý popisek (např. ".max, .3ds")
    description = models.CharField(max_length=30, verbose_name=_("Software"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Software")
        verbose_name_plural = _("Software")

# 3D model
class Model3D(models.Model):
    # Jméno modelu - povinné, max. 50 znaků
    name = models.CharField(max_length=50,
                            verbose_name=_("Name"),
                            help_text=_("Enter the name"),
                            error_messages={"blank": _("Name cannot be empty"),
                                            "max_length": _("Name cannot exceed 50 characters")})

    # Kategorie modelu
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=False,
                                 verbose_name=_("Category"))

    # Datum nahrání - automaticky nastaveno na aktuální datum
    uploaded = models.DateTimeField(auto_now_add=True,
                                    verbose_name=_("Uploaded at"))
    # Datum poslední aktualizace - automaticky aktualizováno při každé změně
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name=_("Date of last update"))
    # Popis modelu - nepovinné pole
    description = models.TextField(blank=True,
                                   null=True,
                                   verbose_name=_("Description"),
                                   help_text=_("Enter a short description of the model"),
                                   error_messages={"max_length": _("Description cannot exceed 1000 characters")})
    # Samotný 3D model
    model = models.FileField(upload_to="models/models/",
                             verbose_name=_("3D model"),
                             help_text=_("Upload the 3D model file (.obj, .fbx..)"),
                             error_messages={"invalid": _("Invalid file format")})
    # Náhledový obrázek modelu (Hlavní náhled)
    thumbnail = models.ImageField(upload_to="models/thumbnails/",
                                  verbose_name=_("Model preview image"),
                                  help_text=_("Upload a preview image for the model"),
                                  error_messages={"invalid": _("Invalid image format")})

    # Připojení tabulky 'User' (tvůrce modelu)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("Creator"))

    # Název modelu jako řetězec
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-uploaded']  # Seřazení podle data nahrání sestupně
        verbose_name = _("3D Model")
        verbose_name_plural = _("3D Models")


# Obrázek 3D modelu (bude z nich tvořena galerie)
class ModelImage(models.Model):
    # Jeden Model3D může mít více obrázků v galerii
    model3d = models.ForeignKey('Model3D', related_name='images', on_delete=models.CASCADE)
    # Obrázek galerie
    image = models.ImageField(upload_to="models/gallery/", verbose_name=_("Gallery Image"))


# Údaje o souboru 3D modelu (vyplní se automaticky při nahrání)
class Data(models.Model):
    # Spojení s 3D modelem
    model3d = models.OneToOneField('Model3D', primary_key=True, on_delete=models.CASCADE, verbose_name=_("3D Model"))

    # Počet ploch/trojúhelníků v modelu
    polygons = models.PositiveIntegerField(verbose_name=_("Number of polygons"))

    # Počet vrcholů v modelu
    vertices = models.PositiveIntegerField(verbose_name=_("Number of vertices"))

    # Velikost souboru v bajtech
    file_size = models.PositiveIntegerField(verbose_name=_("File size (bytes)"))

    # Formát souboru (např. .obj, .fbx...)
    file_format = models.CharField(max_length=10, verbose_name=_("File format"))


# Uživatelské komentáře k 3D modelům
class Comment(models.Model):
    # Autor komentáře
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="comments",
                             verbose_name=_("Author"))
    # Spojení s 3D modelem
    model3d = models.ForeignKey('Model3D',
                                on_delete=models.CASCADE,
                                related_name="comments",
                                verbose_name=_("3D Model"))
    # Obsah komentáře
    content = models.TextField(verbose_name=_("Content"),
                               help_text=_("Enter your comment here"),
                               error_messages={"blank": _("Comment cannot be empty"),
                                               "max_length": _("Comment cannot exceed 2000 characters")})
    # Datum vytvoření komentáře
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_("Created at"))
    # Datum poslední aktualizace komentáře
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_("Updated at"))

    def __str__(self):
        return f"Comment by {self.user.get_username()} on {self.model3d.name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
