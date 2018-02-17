from django.db import models

# Create your models here.


class Product(models.Model):
    image = models.ImageField(verbose_name="Bild", null=True, blank=True)
    title = models.CharField(verbose_name="Titel", max_length=200)
    description = models.TextField(verbose_name="Beschreibung", max_length=200)
