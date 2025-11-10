from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


# Uživatelé a tvůrci 3D modelů
class User(AbstractUser):
    # Profilový obrázek uživatele - nepovinné pole
    picture = models.ImageField(upload_to="profiles/",
                                null=True,
                                blank=True,
                                verbose_name="Profile picture",
                                help_text="Upload a profile picture",
                                error_messages={"invalid": "Invalid image format"})

    # ZMĚNA 1: Přepsání pole groups pro řešení kolize (E304)
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name="users_custom_groups",  # Unikátní jméno
        related_query_name="user",
    )

    # ZMĚNA 2: Přepsání pole user_permissions pro řešení kolize (E304)
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="users_custom_permissions",  # Unikátní jméno
        related_query_name="user",
    )

    def __str__(self):
        return self.username

    class Meta(AbstractUser.Meta):
        ordering = ['username']
        verbose_name = "User"
        verbose_name_plural = "Users"