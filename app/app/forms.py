from django import forms
from pkg_resources import require

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'author']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'author']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Введите Ваш комментарий'}),
            'author': forms.TextInput(attrs={'placeholder': 'Введите Ваше имя'}),
        }