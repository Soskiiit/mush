from django.shortcuts import get_object_or_404
from catalog.models import Photo, Project, Model3D
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import EditProjectForm


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
            for photo in Photo.objects.filter(for_model=project.id):
                photo.delete()

            project.model = Model3D.objects.create()
            
            if 'images' in form.files:
                for image in form.files['images']:
                    photo = Photo.objects.create(for_model=project.model, image=image)
                    photo.save()
                project.model.status = 'empty'

            elif 'model' in form.files:
                print('Loading', form.files['model'])
                project.model.original = form.files['model']
                project.model.lowres = form.files['model']
                project.model.status = 'completed'

            project.model.save()

        project.save()
        return redirect('project', id=id)

    return render(request, 'catalog/item-edit.html', {'form': form, 'project': project})


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
