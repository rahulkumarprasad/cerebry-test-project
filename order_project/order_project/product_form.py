from django.forms import ModelForm
from .models import Products

class ProductForm(ModelForm):
    '''Django model form for creating new product'''
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Products
        fields = ["name", "price", "image", "description"]