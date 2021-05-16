# ProductForm
from django import forms
from .models import Product, ProductType


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'name',
            'product_type',
            'image',
            'price',
            'colour',
            'tag',
            'length',
            'desc',
            'quantity'
        )


# normal form
class SearchForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    product_type = forms.ModelChoiceField(
        queryset=ProductType.objects.all(), required=False)