from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    # Lokální profilový obrázek
    picture = models.ImageField(upload_to="profiles/",
                                null=True,
                                blank=True,
                                verbose_name=_("Profile picture"),
                                help_text=_("Upload a profile picture"),
                                error_messages={"invalid": _("Invalid image format")})

    # URL pro profilový obrázek ze sociálního účtu
    picture_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name=_("Profile Picture URL"),
        help_text=_("URL of profile picture from social account")
    )

    # Přepsání pole groups pro řešení kolize (E304)
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name="users_custom_groups",
        related_query_name="user",
    )

    # Přepsání pole user_permissions pro řešení kolize (E304)
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="users_custom_permissions",
        related_query_name="user",
    )

    # Vrátí profilovou fotku - priorita: URL → lokální → defaultní
    def get_profile_picture(self):
        if self.picture_url:
            return self.picture_url
        # Když se přihlásí přes sociální účet, obrázek se načte z něj
        elif self.picture:
            return self.picture.url
        # Jinak se použije výchozí ikona
        else:
            return '/static/img/icons/user_account.svg'

    def __str__(self):
        return self.username

    class Meta(AbstractUser.Meta):
        ordering = ['username']
        verbose_name = _("User")
        verbose_name_plural = _("Users")
