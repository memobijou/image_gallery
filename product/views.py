from django.shortcuts import render
from django.views import generic
from product import models
# Create your views here.


class ProductListView(generic.ListView):
    template_name = "gallery.html"

    def get_queryset(self):
        return models.Product.objects.all()
