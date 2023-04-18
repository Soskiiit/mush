import pathlib

import Metashape

print(f'im in {pathlib.Path(__file__)}')
import os
from django.conf import settings
from litequeue import LiteQueue
import json
import time
import logging
import sys


ROOT_DIR = pathlib.Path(__file__).parent.parent
sys.path.insert(1, str(ROOT_DIR))
DATABASE_DIR = ROOT_DIR / 'db.sqlite3'
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'mush.settings'
django.setup()

from catalog.models import Project

photogrammetry_queue = LiteQueue(DATABASE_DIR)


def photogrammetry_calc(photo_paths, model_path, project_id):
    try:
        doc = Metashape.Document()
        chunk = doc.addChunk()
        chunk.addPhotos(photo_paths)
        chunk.matchPhotos(
            downscale=1,
            generic_preselection=True,
            reference_preselection=False,
        )
        chunk.alignCameras()
        chunk.buildDepthMaps(downscale=4, filter_mode=Metashape.AggressiveFiltering)
        chunk.buildModel(
            source_data=Metashape.DepthMapsData,
            surface_type=Metashape.Arbitrary,
            interpolation=Metashape.EnabledInterpolation,
        )
        chunk.buildUV(mapping_mode=Metashape.GenericMapping)
        chunk.buildTexture(blending_mode=Metashape.MosaicBlending, texture_size=4096)
        chunk.smoothModel()
        chunk.exportModel(path=os.path.join(model_path, f'model{project_id}_full.glb'))

        chunk.decimateModel(face_count=settings.LOWRES_MODEL_FACE_COUNT)
        chunk.buildUV(mapping_mode=Metashape.GenericMapping, texture_size=2048)
        chunk.buildTexture(blending_mode=Metashape.MosaicBlending, texture_size=1024)
        chunk.exportModel(path=os.path.join(model_path, f'model{project_id}_prev.glb'))
        Project.objects.filter(id=project_id).update(
            status='completed',
            models_highres=os.path.join(
                Path(model_path).parts[-1], f'model{project_id}_full.glb'
            ),
            model_lod=os.path.join(
                Path(model_path).parts[-1], f'model{project_id}_prev.glb'
            ),
        )
    except Exception as ex:
        logging.basicConfig(
            filename='photogrammetry.log',
            level=logging.ERROR,
            format='%(asctime)s %(message)s',
        )
        logging.error(f'{ex} for project with id: {project_id}')
        Project.objects.filter(id=project_id).update(status='error')


if __name__ == '__main__':
    print('Starting worker')
    while True:
        if photogrammetry_queue.empty():
            time.sleep(1)
        else:
            try:
                message = photogrammetry_queue.pop().data
                args = json.loads(message)
                print(f'starting photogrammetry in project {args['project_id']}')
                photogrammetry_calc(**args)
                print('done photogrammetry process')
                if photogrammetry_queue.empty():
                    print('Waiting for tasks')
            except Exception as ex:
                print(f'Caught {ex} during processing project')
