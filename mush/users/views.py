from catalog.models import Project
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import SignupForm
from .models import UserProfile


def signup(request):
    form = SignupForm(request.POST)

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        user.save()
        user_pd = UserProfile.objects.create(for_user=user)
        user_pd.save()
        return redirect('index')

    return render(request, 'users/signup.html', {'form': form})


def login(request):
    return redirect('index')


def logout(request):
    django_logout(request)
    return redirect('index')


def profile(request, id):
    user_projects = Project.objects.filter(owner__id=id)
    if request.user.id != id:
        user_projects = user_projects.filter(is_public=True)

    ctx = {
        'profile': User.objects.get(id=id),
        'projects': user_projects,
    }
    return render(request, 'users/profile.html', ctx)


def my_profile(request):
    ctx = {
        'profile': User.objects.get(id=request.user.id),
        'projects': Project.objects.filter(owner__id=request.user.id),
    }
    return render(request, 'users/my-profile.html', ctx)


def edit_my_profile(request):
    return render(request, 'users/edit-my-profile.html', {})
