import json
import os

from catalog.models import Model3D, Photo
from django.conf import settings
from litequeue import LiteQueue

photogrammetry_queue = LiteQueue(settings.DATABASE_DIR)


def photogrammetry_args_to_json(photo_paths, model_path, model_id):
    return json.dumps(
        {
            'photo_paths': photo_paths,
            'model_path': model_path,
            'model_id': model_id,
        }
    )


def json_to_photogrammetry_args(json_message):
    return json.loads(json_message)


def run_photogrammetry_thread(model_id):
    if not settings.ENABLE_PHOTOGRAMMETRY:
        return

    photo_paths = Photo.objects.filter(for_model_id=model_id).values_list(
        'image', flat=True
    )
    photo_paths = [
        os.path.join(settings.MEDIA_ROOT, cur_photo_path)
        for cur_photo_path in photo_paths
    ]
    model_path = os.path.join(settings.MEDIA_ROOT, 'models')
    Model3D.objects.filter(id=model_id).update(status='in_queue')
    photogrammetry_queue.put(
        photogrammetry_args_to_json(photo_paths, model_path, model_id)
    )
    return model_path
