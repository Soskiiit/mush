from catalog.models import Project
from django.shortcuts import redirect, render


def index(request):
    ctx = {
        'projects': Project.objects.filter(
            is_public=True, status='completed'
        )
    }
    return render(request, 'catalog/index.html', ctx)


def project(request, id):
    ctx = {
        'project': Project.objects.get(id=id),
    }
    return render(request, 'catalog/item-details.html', ctx)


def project_edit(request, id):
    if request.method == 'POST':
        print(request.POST)
        return redirect('project', id=id)

    ctx = {
        'project': Project.objects.get(id=id),
    }
    return render(request, 'catalog/item-edit.html', ctx)
