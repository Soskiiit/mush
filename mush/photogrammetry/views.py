from django.shortcuts import HttpResponse
from mush.settings import ENABLE_PHOTOGRAMMETRY

from .tools import run_photogrammetry_thread


def run_photogrammetry(request, model_id):
    if ENABLE_PHOTOGRAMMETRY:
        model_path = run_photogrammetry_thread(model_id)
        return HttpResponse(
            '<h1>Your model is processing and will be able for download at'
            ' {0}.</h1>'.format(model_path)
        )
    return HttpResponse(
        '<h1>sorry, no photogrammetry yet... Working on it</h1>'
    )
