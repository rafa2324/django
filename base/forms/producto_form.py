'''
created by edgard.ramos (ismytv@gmail.com)
generated by alice.bash.v.2203a
jue 11 ago 2022 23:06:51 -05
'''
from django import forms
from django.utils.translation import gettext_lazy as _
#from django.core.exceptions import ValidationError
from base.models import Producto

 
class ProductoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_data()

    def set_data(self):
        self.fields['desc'].widget.attrs['autofocus'] = True

    class Meta:
        model = Producto
        fields = ['desc']

        error_messages = {
            'desc': {
                'unique': _("Ya existe rubro con esa descripción."),
            },
        }

    def clean(self):
        return super().clean()
    
    def clean_desc(self):
        data = self.cleaned_data['desc'].strip().upper()
        try:
            reg = Producto.objects.get(desc=data)
            if not self.instance.id or self.instance.id != reg.id:
                raise forms.ValidationError('Ya existe otro registro con esa descripción')
        except Producto.DoesNotExist:
            pass

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data