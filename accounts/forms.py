from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2",'first_name','last_name')

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class LoginForm(forms.ModelForm):
    '''Simple login form'''
    class Meta:
        model = User
        fields = ('username', 'password')