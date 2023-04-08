import os
import shutil
import threading
from pathlib import Path

from django.core.mail import send_mail
from mush.settings import ENABLE_PHOTOGRAMMETRY

if ENABLE_PHOTOGRAMMETRY:
    import Metashape


def photogrammetry_main_thread(photo_path, model_path, user):
    photos = [
        os.path.join(photo_path, cur_photo)
        for cur_photo in os.listdir(photo_path)
    ]

    doc = Metashape.Document()
    chunk = doc.addChunk()
    chunk.addPhotos(photos)
    chunk.matchPhotos(
        downscale=1, generic_preselection=True, reference_preselection=False
    )
    chunk.alignCameras()
    chunk.buildDepthMaps(
        downscale=4, filter_mode=Metashape.AggressiveFiltering
    )
    chunk.buildModel(
        source_data=Metashape.DepthMapsData,
        surface_type=Metashape.Arbitrary,
        interpolation=Metashape.EnabledInterpolation,
    )
    chunk.buildUV(mapping_mode=Metashape.GenericMapping)
    chunk.buildTexture(
        blending_mode=Metashape.MosaicBlending, texture_size=4096
    )
    chunk.exportModel(path=model_path)
    if user.is_authenticated:
        send_mail(
            'Your model is ready',
            'Congratulations, {0}, your model is ready for download'.format(
                [user.username]
            ),
            'fill_this@ya.ru',
            [user.email],
            fail_silently=False,
        )
    else:
        send_mail(
            'Your model is ready',
            'Congratulations, {0}, your model is ready for download'.format(
                'no username cuz user is poo'
            ),
            'fill_this@ya.ru',
            ['user@mail.ru'],
            fail_silently=False,
        )


def run_photogrammetry_thread(photos, user):
    if not ENABLE_PHOTOGRAMMETRY:
        return None
    temp_dir_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'temp/'
    )
    photo_path = os.path.join(temp_dir_path, 'photos/')

    if os.path.isdir(temp_dir_path):
        shutil.rmtree(temp_dir_path)

    Path(temp_dir_path).mkdir(parents=True, exist_ok=True)
    Path(photo_path).mkdir(parents=True, exist_ok=True)

    for i in range(len(photos)):
        photos[i].save(photo_path + 'photo_' + str(i) + '.jpg')

    model_path = os.path.join(temp_dir_path, 'model.glb')
    photogrammetry_thread = threading.Thread(
        target=photogrammetry_main_thread, args=(photo_path, model_path, user)
    )
    photogrammetry_thread.start()

    return model_path
