from catalog.models import Project
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


def user(request, id):
    ctx = {
        'observed_user': User.objects.get(id=id),
        'projects': Project.objects.filter(owner__id=id),
    }
    return render(request, 'users/profile.html', ctx)


def profile(request):
    return user(request, request.user.id)


def profile_edit(request):
    return render(request, 'users/profile-edit.html', {})


def projects(request):
    if request.method == 'POST':
        print(request.POST)
        return redirect('my-projects')

    ctx = {
        'projects': Project.objects.all()
    }
    return render(request, 'catalog/my-projects.html', ctx)


def project(request, id):
    ctx = {
        'project': Project.objects.get(id=id),
    }
    return render(request, 'catalog/item-details.html', ctx)


def catalog(request):
    ctx = {
        'projects': Project.objects.filter(
            is_public=True, status='completed'
        )
    }
    return render(request, 'catalog/index.html', ctx)


def project_edit(request, id):
    if request.method == 'POST':
        print(request.POST)
        return redirect('project', id=id)

    ctx = {
        'project': Project.objects.get(id=id),
    }
    return render(request, 'catalog/item-edit.html', ctx)
