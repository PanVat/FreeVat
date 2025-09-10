from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True, blank=False)
    nickname = models.CharField(max_length=30, unique=True, blank=False)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)