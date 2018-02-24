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
        print(f"{table.header} : {table.content}")
        return super().post(request, *args, **kwargs)

    def table_data_to_product_model(self, model, table, replace_header=None):
        header = table.header
        if replace_header:
            header = replace_header
        content = table.content
        bulk_instances = []

        for row in content:
            query_objects = Q()
            for k, v in zip(header, row):
                query_objects &= Q(**{k: v})
                bulk_instances.append(model(**{k: v}))
            print(bulk_instances)
            # bulk_instances.append(row)

        model.objects.bulk_create(bulk_instances)

    def get_table_from_csv_sheet(self, content):
        content = content.decode('utf8')
        sheet = pyexcel.Sheet()
        sheet.csv = content
        table = self.get_table_csv(sheet)
        return table

    def get_table_from_excel_sheet(self, content):
        sheet = pyexcel.get_sheet(file_type="xlsx", file_content=content)
        table = self.get_table_excel(sheet)
        return table

    def get_sheet_header_csv(self, sheet):
        th = (sheet.row[0])[0].replace(u'\ufeff', '')
        header = th.split(";")
        return header

    def get_sheet_content_csv(self, sheet):
        sheet.name_columns_by_row(0)
        content = []
        for row in sheet.row:
            row = row[0].replace(u'\ufeff', '')
            row = row.split(";")
            if self.is_empty_row(row) is False:
                content.append(row)
        return content

    def is_empty_row(self, row):
        for col in row:
            if col != "":
                return False
        return True

    def get_table_csv(self, sheet):
        header = self.get_sheet_header_csv(sheet)
        content = self.get_sheet_content_csv(sheet)
        Table = collections.namedtuple('Table', 'header content')
        table = Table(header=header, content=content)
        return table

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
        if filetype == "csv":
            return self.get_table_from_csv_sheet(content)
        elif filetype == "xlsx":
            return self.get_table_from_excel_sheet(content)
