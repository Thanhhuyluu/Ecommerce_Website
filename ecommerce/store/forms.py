from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Customer


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'example123'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': '••••••••'
    }))


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'example123@gmail.com'
    }))
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nguyen Van A'
    }))

    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'example123'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': '••••••••'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': '••••••••'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Customer.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                email=self.cleaned_data['email']
            )
        return user