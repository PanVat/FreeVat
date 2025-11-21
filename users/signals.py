from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount


@receiver(post_save, sender=SocialAccount)
def update_social_profile_picture(sender, instance, created, **kwargs):
    """Automaticky ulož profilovou fotku z OAuth"""
    user = instance.user

    if instance.provider == 'google':
        extra_data = instance.extra_data
        if 'picture' in extra_data:
            user.picture_url = extra_data['picture']
            user.save()
    elif instance.provider == 'github':
        extra_data = instance.extra_data
        if 'avatar_url' in extra_data:
            user.picture_url = extra_data['avatar_url']
            user.save()