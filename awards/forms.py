from django import forms
from .models import Profile , Project, Review

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

class UploadForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user','likes','upload_date','profile']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ['user','comment_date','image',]
