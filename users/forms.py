from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Create your forms here.



class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['login', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"placeholder": field.label})



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label=_("Email"), required=True)

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"placeholder": field.label})

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An user with this email already exists!")
        return email
