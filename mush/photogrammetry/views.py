import os

from PIL import Image
from django.shortcuts import HttpResponse

from .tools import photos_to_model


def run_process(request):
    # LOAD EXAMPLE PHOTOS:
    photo_dir = "fD:\\Media\\Photos\\Photogram\\examples\\Meshroom_6_monstree"
    photo_paths = [
        os.path.join(photo_dir, cur_photo)
        for cur_photo in os.listdir(photo_dir)
    ]
    photos = [Image.open(cur_photo_path) for cur_photo_path in photo_paths]

    model_path = photos_to_model(photos)
    return HttpResponse('<h1>Done, models is in {0}</h1>'.format(model_path))
