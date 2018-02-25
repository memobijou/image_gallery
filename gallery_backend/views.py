from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic
from gallery_backend.forms import ProductForm, ImportForm
from product.models import Product
from django.views.generic.base import ContextMixin
import pyexcel
import collections


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
    success_url = reverse_lazy("backend-list")


class ProductList(ProductListMixin, generic.ListView):
    template_name = "gallery_backend/list_products.html"

    def get_queryset(self):
        return Product.objects.all().order_by("-id")


class ProductUpdate(generic.UpdateView):
    model = Product
    fields = "__all__"
    template_name = "gallery_backend/create_product.html"
    success_url = reverse_lazy("backend-list")

    def get_object(self):
        return Product.objects.get(pk=self.kwargs.get("pk"))


class ProductDeleteView(generic.DeleteView):
    template_name = 'confirm_delete_someitems.html'
    model = Product
    success_url = reverse_lazy('backend-list')

    def get_object(self):
        super().get_object()
        object_ = Product.objects.get(pk=self.kwargs.get("pk"))
        return object_


class ExcelImportView(generic.FormView):
    template_name = "gallery_backend/import_excel.html"
    form_class = ImportForm
    success_url = reverse_lazy("backend-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["title"] = "Import"
        return context

    def post(self, request, *args, **kwargs):
        content = request.FILES["excel_field"].read()
        file_type = str(request.FILES["excel_field"]).split(".")[1]
        table = self.get_table(content, file_type)
        self.table_data_to_product_model(Product, table,
                                         ["supplier", "description", "ean", "amount", "price", "purchase_price"])
        return super().post(request, *args, **kwargs)

    def table_data_to_product_model(self, model, table, replace_header=None):
        header = table.header
        if replace_header:
            header = replace_header
        content = table.content

        bulk_instances = []
        for row in content:
            dict_ = {}
            for k, v in zip(header, row):
                dict_[k] = v
            bulk_instances.append(model(**dict_))
        model.objects.bulk_create(bulk_instances)

    def is_empty_row(self, row):
        for col in row:
            if col != "":
                return False
        return True

    def get_table_excel(self, sheet):
        Table = collections.namedtuple('Table', 'header content')
        header = sheet.row[0]
        sheet.name_columns_by_row(0)
        content = []
        for row in sheet.row:
            if self.is_empty_row(row) is False:
                content.append(row)
        table = Table(header=header, content=content)
        return table

    def get_table(self, content, filetype):
        if filetype == "xlsx":
            sheet = pyexcel.get_sheet(file_type="xlsx", file_content=content)
            table = self.get_table_excel(sheet)
        elif filetype == "xls":
            sheet = pyexcel.get_sheet(file_type="xls", file_content=content)
            table = self.get_table_excel(sheet)
        else:
            return
        return table

