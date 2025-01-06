from enum import unique

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import Post, Comment, User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Введите Ваш комментарий'}),
        }

class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    username = forms.CharField(required=True,
                               min_length=4,
                               widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():  # Проверка на уникальность
            raise ValidationError("Пользователь с таким email уже зарегистрирован.")
        return email