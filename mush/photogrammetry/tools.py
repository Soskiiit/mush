import json
import os

from catalog.models import Photo, Project
from django.conf import settings
from litequeue import LiteQueue

photogrammetry_queue = LiteQueue(settings.DATABASE_DIR)


def photogrammetry_args_to_json(photo_paths, model_path, project_id):
    return json.dumps(
        {
            'photo_paths': photo_paths,
            'model_path': model_path,
            'project_id': project_id,
        }
    )


def json_to_photogrammetry_args(json_message):
    return json.loads(json_message)


def run_photogrammetry_thread(project_id):
    if not settings.ENABLE_PHOTOGRAMMETRY:
        return

    photo_paths = Photo.objects.filter(for_project_id=project_id).values_list(
        'image', flat=True
    )
    photo_paths = [
        os.path.join(settings.MEDIA_ROOT, cur_photo_path)
        for cur_photo_path in photo_paths
    ]

    model_path = os.path.join(settings.MEDIA_ROOT, 'models')
    photogrammetry_queue.put(
        photogrammetry_args_to_json(photo_paths, model_path, project_id)
    )
    Project.objects.filter(id=project_id).update(status='in_progress')

    return model_path
