from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(verbose_name="Titel", max_length=200)
    description = models.CharField(verbose_name="Beschreibung", max_length=200)
