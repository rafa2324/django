from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from base.models import User

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

        field_args = {
            "name" : {
                "error_messages" : {
                    "required" : "Please let us know what to call you!"
                }
            }
        }

    def clean(self) :
        data = self.cleaned_data.get('name')
        print(data)
        if "gar" not in data:
            print('errorrrr')
            self._errors['name'] = self.error_class(['A minimum of 5 characters is required'])
            raise ValidationError("You have forgotten about Fred!")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return self.cleaned_data


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['image_file', 'name', 'username', 'email', 'modo_apariencia']
 