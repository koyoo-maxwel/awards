from django import forms
from .models import Profile, Project, Review
from django.contrib.auth.models import User


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'profile_pic',
            'contact',
            'bio'
        ]


class UploadForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user', 'upload_date', 'profile']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ['user', 'comment_date', 'image', ]
