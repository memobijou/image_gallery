from django.forms import ModelForm
from product.models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ignore_fields = ["image"]
        for field in self.fields:
            if field in ignore_fields:
                continue
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
