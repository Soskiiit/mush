import logging
import os
import time
from pathlib import Path

import Metashape
import adj_django_connection
from catalog.models import Project
from django.conf import settings
from litequeue import LiteQueue
from tools import json_to_photogrammetry_args

DATABASE_DIR = adj_django_connection.ROOT_DIR / 'db.sqlite3'


photogrammetry_queue = LiteQueue(DATABASE_DIR)

logging.basicConfig(
    filename='photogrammetry.log',
    level=logging.ERROR,
    format='%(asctime)s %(message)s',
)
photogrametry_logger = logging.getLogger('photogrammetry_logger')


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
        chunk.buildDepthMaps(
            downscale=4, filter_mode=Metashape.AggressiveFiltering
        )
        chunk.buildModel(
            source_data=Metashape.DepthMapsData,
            surface_type=Metashape.Arbitrary,
            interpolation=Metashape.EnabledInterpolation,
        )
        chunk.smoothModel()
        chunk.buildUV(mapping_mode=Metashape.GenericMapping)
        chunk.buildTexture(
            blending_mode=Metashape.MosaicBlending, texture_size=4096
        )

        chunk.exportModel(
            path=os.path.join(model_path, f'model{project_id}_full.glb')
        )
        model_stats = chunk.model.statistics()
        face_count = model_stats.faces
        vert_count = model_stats.vertices

        chunk.decimateModel(face_count=settings.LOWRES_MODEL_FACE_COUNT)
        chunk.buildUV(mapping_mode=Metashape.GenericMapping, texture_size=2048)
        chunk.buildTexture(
            blending_mode=Metashape.MosaicBlending, texture_size=1024
        )
        chunk.exportModel(
            path=os.path.join(model_path, f'model{project_id}_prev.glb')
        )

        Project.objects.filter(id=project_id).update(
            status='completed',
            models_highres=os.path.join(
                Path(model_path).parts[-1], f'model{project_id}_full.glb'
            ),
            model_lod=os.path.join(
                Path(model_path).parts[-1], f'model{project_id}_prev.glb'
            ),
            faces=face_count,
            vertices=vert_count,
        )

    except Exception as ex:
        photogrametry_logger.error(f'{ex} for project with id: {project_id}')
        Project.objects.filter(id=project_id).update(status='error')


if __name__ == '__main__':
    print('Waiting for tasks')
    photogrametry_logger.info('Waiting for tasks')
    while True:
        if photogrammetry_queue.empty():
            time.sleep(1)
        else:
            try:
                message = photogrammetry_queue.pop().data
                args = json_to_photogrammetry_args(message)
                photogrametry_logger.info(
                    f'starting photogrammetry in project {args["project_id"]}'
                )
                photogrammetry_calc(**args)
                photogrametry_logger.info(
                    f'done photogrammetry in project {args["project_id"]}'
                )
                if photogrammetry_queue.empty():
                    print('Waiting for tasks')
            except Exception as ex:
                print(f'caught {ex} during photogrammetry process')
                photogrametry_logger.error(
                    f'caught {ex} during photogrammetry process'
                )
