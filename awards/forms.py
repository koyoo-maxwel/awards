from django import forms
from .models import Profile , Project , Comment

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

class UploadForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user','likes','upload_date','profile']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['user','comment_date','image',]
