from django.urls import reverse_lazy
from django.views import generic
from gallery_backend.forms import ProductForm


class ProductCreate(generic.CreateView):
    form_class = ProductForm
    template_name = "gallery_backend/create_form.html"
    success_url = reverse_lazy("gallery")
