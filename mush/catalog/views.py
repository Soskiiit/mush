from catalog.models import Photo, Project
from django.shortcuts import redirect, render
from photogrammetry.tools import run_photogrammetry_thread


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
    project_query = Project.objects.filter(
        owner__id=request.user.id, id=id
    )

    if request.method == 'POST' and project_query.exists():
        project = project_query[0]
        if 'delete' in request.POST:
            project.delete()
            return redirect('my-profile')

        project.name = request.POST['name']
        # project.public =
        for image in request.FILES.getlist('images'):
            photo = Photo.objects.create(for_project=project, image=image)
            photo.save()
            print('added', image)
        project.save()

        run_photogrammetry_thread(project.id)
        return redirect('project', id=id)

    ctx = {
        'project': Project.objects.get(id=id),
    }
    return render(request, 'catalog/item-edit.html', ctx)


def project_create(request):
    if request.user.is_authenticated:
        ctx = {
            'project': Project.objects.create(
                name='New project',
                owner=request.user
            ),
        }
        return render(request, 'catalog/item-edit.html', ctx)
    return redirect('index')
