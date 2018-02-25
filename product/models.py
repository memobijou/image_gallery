from django.db import models

# Create your models here.


class Product(models.Model):
    image = models.ImageField(verbose_name="Bild", null=True, blank=True)
    title = models.CharField(verbose_name="Titel", max_length=200, null=True, blank=True)
    supplier = models.CharField(verbose_name="Hersteller", max_length=200, null=True, blank=True)
    description = models.TextField(verbose_name="Beschreibung", max_length=400, null=True, blank=True)
    ean = models.CharField(verbose_name="EAN", max_length=200, null=True, blank=True)
    amount = models.CharField(verbose_name="Menge", max_length=200, null=True, blank=True)
    price = models.CharField(verbose_name="Preis", max_length=200, null=True, blank=True)
    purchase_price = models.CharField(verbose_name="2018", max_length=200, null=True, blank=True)
