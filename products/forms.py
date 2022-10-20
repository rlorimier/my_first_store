from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # the categories to show up in the form using their friendly name.
        categories = Category.objects.all()
        # to create a list of tuples of the friendly names associated with their category ids. This special syntax is called the list comprehension.
        # And is just a shorthand way of creating a for loop that adds items to a list.
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        # Instead of seeing the category ID or the name field we'll see the friendly name.
        self.fields['category'].choices = friendly_names
        # just iterate through the rest of these fields and set some classes on them to make them match the theme of the rest of our store.
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
