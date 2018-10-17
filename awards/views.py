from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from .models import Project, Profile, Review
from django.contrib.auth.models import User
from .forms import EditProfileForm, UploadForm, ReviewForm, UserEditForm

# Create your views here.


@login_required(login_url='/accounts/login/')
def home(request):
    profile = Profile.objects.get(user=request.user)
    projects = Project.get_projects()
    for project in projects:
        print(project.project_image)

    data = {"profile": profile,
            "projects": projects,
            "profile": profile,
            }
    return render(request, 'index.html', data)


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

    if request.method == 'POST':
        pro_form = EditProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        user_form = UserEditForm(request.POST, instance=request.user)

        if pro_form.is_valid() and user_form.is_valid():
            profile = pro_form.save(commit=False)
            up_user = user_form.save(commit=False)
            # update.user = current_user
            profile.save()
            up_user.save()
            return redirect('profile')
    else:
        pro_form = EditProfileForm(instance=request.user.profile)
        user_form = UserEditForm(instance=request.user)
    return render(request, 'profile/edit.html', {"title": title, "pro_form": pro_form, "user_form": user_form})


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
    title = 'Awards'
    current_user = request.user

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


@login_required(login_url='/accounts/login/')
def review(request, project_id=None):
    if request.method == 'POST':
        # project = Project.objects.get(project, pk=project_id)
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('home')
    else:
        form = ReviewForm()
        # project = Project.objects.get(pk=project_id)
        project = get_object_or_404( Project ,pk=project_id)
        try:
            review = Review.objects.get(project__pk=project_id)
        except:
            review = None

        return render(request, 'review/review.html', {"review": review, "project": project, 'form': form})
