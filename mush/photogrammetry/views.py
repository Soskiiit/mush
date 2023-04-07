import os

from PIL import Image
from django.shortcuts import HttpResponse
from mush.settings import ENABLE_PHOTOGRAMMETRY

from .tools import photos_to_model


def run_process(request):
    if ENABLE_PHOTOGRAMMETRY:
        # LOAD EXAMPLE PHOTOS:
        photo_dir = 'D:/Media/Photos/Photogram/stolb1'
        photo_paths = [
            os.path.join(photo_dir, cur_photo)
            for cur_photo in os.listdir(photo_dir)
        ]
        photos = [Image.open(cur_photo_path) for cur_photo_path in photo_paths]

        model_path = photos_to_model(photos)
        return HttpResponse(
            '<h1>Done, models is in {0}</h1>'.format(model_path)
        )
    else:
        return HttpResponse(
            '<h1>sowwy, no photogrammetry yet... Working on it</h1>'
        )
