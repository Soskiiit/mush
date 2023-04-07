import os

from PIL import Image
from django.shortcuts import HttpResponse

from .tools import photos_to_model


def run_process(request):
    photo_dir = (
        'D:\Media\Photos\Photogram\examples\Meshroom_6_monstree'  # JUST FOR EXAMPLE
    )
    photo_paths = [
        os.path.join(photo_dir, cur_photo) for cur_photo in os.listdir(photo_dir)
    ]  # JUST FOR EXAMPLE
    photos = [
        Image.open(cur_photo_path) for cur_photo_path in photo_paths
    ]  # JUST FOR EXAMPLE

    model_path = photos_to_model(photos)
    return HttpResponse('<h1>Done, models is in {0}</h1>'.format(model_path))
