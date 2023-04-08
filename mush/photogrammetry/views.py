import os

from PIL import Image
from django.shortcuts import HttpResponse
from mush.settings import ENABLE_PHOTOGRAMMETRY

from .tools import run_photogrammetry_thread


def run_photogrammetry(request):
    if ENABLE_PHOTOGRAMMETRY:
        # LOAD EXAMPLE PHOTOS:
        photo_dir = 'D:/Media/Photos/Photogram/examples/monstree_3'
        photo_paths = [
            os.path.join(photo_dir, cur_photo)
            for cur_photo in os.listdir(photo_dir)
        ]
        photos = [Image.open(cur_photo_path) for cur_photo_path in photo_paths]
        model_path = run_photogrammetry_thread(photos, request.user)
        return HttpResponse(
            '<h1>Your model is processing and will be able for download at'
            ' {0}. We`ll notify you by email</h1>'.format(model_path)
        )
    else:
        return HttpResponse(
            '<h1>sowwy, no photogrammetry yet... Working on it</h1>'
        )
