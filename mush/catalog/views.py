from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from photogrammetry.tools import run_photogrammetry_thread

from .forms import EditProjectForm
from .models import Model3D, Photo, Project


def index(request):
    ctx = {
        'projects': Project.objects.filter(
            is_public=True, model__status='completed'
        )
    }
    return render(request, 'catalog/index.html', ctx)


def project(request, id):
    ctx = {
        'project': get_object_or_404(Project, id=id),
    }
    return render(request, 'catalog/item-details.html', ctx)


def project_edit(request, id):
    project = get_object_or_404(Project, id=id)

    form = EditProjectForm(
        initial={'name': project.name, 'public': project.is_public}
    )

    if request.method == 'POST':
        form = EditProjectForm(request.POST, request.FILES)

        if not form.is_valid():
            messages.error(request, 'Invalid form input', fail_silently=True)
            return redirect('project-edit', id=id)

        project.name = form.cleaned_data['name']
        project.is_public = form.cleaned_data['public']

        if form.files:
            if project.model:
                project.model.delete()

            project.model = Model3D.objects.create()

            if 'images' in form.files:
                for image in form.files.getlist('images'):
                    photo = Photo.objects.create(
                        for_model=project.model,
                        image=image
                    )
                    photo.save()
                run_photogrammetry_thread(project.model.id)

            elif 'model' in form.files:
                print('Model:', form.files['model'])
                project.model.original = form.files['model']
                project.model.lowres = form.files['model']
                project.model.status = 'completed'

        project.save()
        return redirect('project', id=id)

    return render(
        request,
        'catalog/item-edit.html',
        {'form': form, 'project': project}
    )


def project_create(request):
    if request.user.is_authenticated:
        project = Project.objects.create(
            name='New project',
            owner=request.user,
        )
        ctx = {
            'project': project,
            'form': EditProjectForm(
                initial={'name': project.name, 'public': project.is_public}
            )
        }
        return render(request, 'catalog/item-edit.html', ctx)
    return redirect('index')
