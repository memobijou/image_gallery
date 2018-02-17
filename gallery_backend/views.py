from django.urls import reverse_lazy
from django.views import generic
from gallery_backend.forms import ProductForm
from product.models import Product
from django.views.generic.base import ContextMixin


class ProductCreateMixin(ContextMixin):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.extra_context["title"] = "Erstellen"
        context.update(self.extra_context)
        return context


class ProductListMixin(ContextMixin):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.extra_context["title"] = "Ansicht"

        field_verbose_names = [f.verbose_name for f in Product._meta.get_fields()]

        # ID löschen
        del field_verbose_names[0]
        self.extra_context["field_verbose_names"] = field_verbose_names
        field_names = [f.name for f in Product._meta.get_fields()]

        # ID löschen
        del field_names[0]
        self.extra_context["field_names"] = field_names
        context.update(self.extra_context)
        return context


class ProductCreate(ProductCreateMixin, generic.CreateView):
    form_class = ProductForm
    template_name = "gallery_backend/create_product.html"
    success_url = reverse_lazy("gallery")


class ProductList(ProductListMixin, generic.ListView):
    template_name = "gallery_backend/list_products.html"

    def get_queryset(self):
        return Product.objects.all()
