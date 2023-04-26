from django.contrib import messages
from django.http import FileResponse, Http404
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from photogrammetry.tools import run_photogrammetry_thread

from .forms import EditProjectForm
from .models import Model3D, Photo, Project
from .utils import get_gltf_metadata


def index(request):
    ctx = {
        'projects': Project.objects.filter(
            is_public=True, model__status='completed'
        )
    }
    return render(request, 'catalog/index.html', ctx)


def list(request):
    ctx = {
        'projects': Project.objects.filter(
            is_public=True, model__status='completed'
        )
    }
    return render(request, 'catalog/list.html', ctx)


def project(request, id):
    ctx = {
        'project': get_object_or_404(Project, id=id),
    }
    return render(request, 'catalog/item-details.html', ctx)


def project_last_update(request, id):
    last_update_time = (Project.objects
                        .filter(id=id)
                        .values_list('model__last_update_date', flat=True))
    if last_update_time:
        return HttpResponse(last_update_time[0]
                            .strftime('%d/%m/%Y %H:%M:%S:%f'))


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
            project.download_count = 0

            if 'images' in form.files:
                for image in form.files.getlist('images'):
                    photo = Photo.objects.create(
                        for_model=project.model,
                        image=image
                    )
                    photo.save()
                run_photogrammetry_thread(project.model.id)

            elif 'model' in form.files:
                project.model.original = form.files['model']
                project.model.lowres = form.files['model']
                project.model.status = 'completed'
                project.model.save()

                gltf_meta = get_gltf_metadata(project.model.original.path)
                project.model.vertex_count = gltf_meta.vertex_count
                # Not implemented yet (it's tricky)
                # project.model.face_count = gltf_meta.face_count
                project.model.save()

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


def project_download(request, id):
    project = get_object_or_404(
        Project,
        id=id,
        model__status='completed',
    )
    if not project.is_public and request.user != project.owner:
        raise Http404()

    project.download_count += 1
    project.save()
    return FileResponse(open(project.model.original.path, 'rb'))


def project_delete(request, id):
    if not request.user.is_authenticated:
        return Http404()

    project = get_object_or_404(Project, id=id, owner=request.user)
    project.delete()

    return redirect('my-profile')
