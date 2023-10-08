from django import forms
from .models import (
    PublishedModel, TitleModel, Category, Location, Post, Comment
)
from django.contrib.auth import get_user_model

User = get_user_model()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'pub_date', 'category', 'location', 'image']
        widgets = {'pub_date': forms.DateInput(attrs={'type': 'date'})}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class EditCommentForm(forms.ModelForm):
    post_id = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = Comment
        fields = ['text']

    def set_post_id(self, post_id):
        self.fields['post_id'].initial = post_id


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


class PublishedModelForm(forms.ModelForm):
    class Meta:
        model = PublishedModel
        fields = ['is_published']


class TitleModelForm(forms.ModelForm):
    class Meta:
        model = TitleModel
        fields = ['title']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['description', 'slug']


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name']
