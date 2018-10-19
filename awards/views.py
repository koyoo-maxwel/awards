from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from .models import Project, Profile, Review
from django.contrib.auth import login, authenticate
from .forms import SignupForm, EditProfileForm, UploadForm, ReviewForm, UserEditForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            profile = Profile(user=user)
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')

    else:
        return HttpResponse('Activation link is invalid!')


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
        message = "are you sure is a registered user here?"
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
        project = get_object_or_404(Project, pk=project_id)
        review = Review.objects.filter(project__pk=project_id)
        print(review)

        return render(request, 'review/review.html', {"review": review, "project": project, 'form': form})
