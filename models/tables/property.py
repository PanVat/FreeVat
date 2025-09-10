from django.db import models

class Property(models.Model):
    polygon_count = models.IntegerField()
    vertex_count = models.IntegerField()
    file_size = models.IntegerField()
    file_format = models.CharField(max_length=50)
    format_suffix = models.CharField(max_length=5)