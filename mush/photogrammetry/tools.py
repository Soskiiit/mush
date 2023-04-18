import json
import os

from catalog.models import Photo, Project
from django.conf import settings
from litequeue import LiteQueue

photogrammetry_queue = LiteQueue(settings.DATABASE_DIR)


def run_photogrammetry_thread(project_id):
    if not settings.ENABLE_PHOTOGRAMMETRY:
        return

    use_local_photos = False

    if use_local_photos:
        photo_path = 'D:/Media/Photos/Photogram/examples/Meshroom_6_monstree'

        photo_paths = [
            os.path.join(photo_path, cur_photo)
            for cur_photo in os.listdir(photo_path)
        ]
    else:
        photo_paths = Photo.objects.filter(
            for_project_id=project_id
        ).values_list('image', flat=True)
        photo_paths = [
            os.path.join(settings.MEDIA_ROOT, cur_photo_path)
            for cur_photo_path in photo_paths
        ]

    model_path = os.path.join(settings.MEDIA_ROOT, 'models')
    photogrammetry_queue.put(
        json.dumps(
            {
                'photo_paths': photo_paths,
                'model_path': model_path,
                'project_id': project_id,
            }
        )
    )
    Project.objects.filter(id=project_id).update(status='in_progress')

    return model_path
