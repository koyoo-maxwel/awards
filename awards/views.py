from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from .models import Project, Profile, Review
from django.contrib.auth.models import User
from .forms import EditProfileForm, UploadForm, ReviewForm

# Create your views here.


@login_required(login_url='/accounts/login/')
def home(request):
    current_user = request.user
    project = Project.get_projects()
    return render(request, 'index.html', {"current_user": current_user,
                                          "project": project, })


@login_required(login_url='/accounts/login/')
def profile(request):
    user = request.user
    profile = Profile.get_profile(user)

    data = {
        "profile": profile,

    }
    print(data)

    return render(request, 'profile/profile.html', data)


@login_required(login_url='/accounts/login/')
def edit(request):
    title = 'awards'
    current_user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            update = form.save(commit=False)
            update.user = current_user
            update.save()
            return redirect('profile')
    else:
        form = EditProfileForm()
    return render(request, 'profile/edit.html', {"title": title,
                                                 "form": form})


@login_required(login_url="/accounts/login/")
def search_results(request):
    current_user = request.user
    # profile = Profile.get_profile()
    if 'username' in request.GET and request.GET["username"]:
        search_term = request.GET.get("username")
        # searched = Profile.find_profile(search_term)
        searched = User.objects.filter(username__icontains=search_term)

        message = search_term

        return render(request, 'search.html', {"message": message,
                                               "profiles": profile,
                                               "user": current_user,
                                               "searched": searched})
    else:
        message = "You haven't searched for any user"
        return render(request, 'search.html', {"message": message})


@login_required(login_url="/accounts/login/")
def upload(request):
    title = 'Instagram'
    current_user = request.user
    for profile in profiles:
        if profile.user.id == current_user.id:
            if request.method == 'POST':
                form = UploadForm(request.POST, request.FILES)
                if form.is_valid():
                    upload = form.save(commit=False)
                    upload.user = current_user
                    upload.profile = profile
                    upload.save()
                    return redirect('home')
            else:
                form = UploadForm()
            return render(request, 'upload/new.html', {"title": title,
                                                       "user": current_user,
                                                       "form": form})
