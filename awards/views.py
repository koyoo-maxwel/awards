from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,Http404
from .models import Project,Profile,Comment
from django.contrib.auth.models import User
from .forms import EditProfileForm,UploadForm,CommentForm

# Create your views here.

@login_required(login_url='/accounts/login/')
def home(request):
    current_user = request.user
    profile = Profile.get_profile()
    project = Project.get_projects()
    comments = Comment.get_comment()
    return render(request,'index.html',{"profile":profile,
                                        "comments":comments,
                                        "current_user":current_user,
                                        "project":project,})




@login_required(login_url='/accounts/login/')
def profile(request):
    
    current_user = request.user
    profile_pic = Profile.get_profile()
    
    comments = Comment.get_comment()

    data = {
        "comments":comments,
        "profile_pic":profile_pic,
        "user":current_user,
        "profile":profile,
    }
    
    return render(request,'profile/profile.html',data)