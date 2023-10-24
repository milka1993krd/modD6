from django.forms import ModelForm, BooleanField, ModelChoiceField
from django import forms
from .models import Post, Category


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'postType', 'postCategory', 'title', 'text']
