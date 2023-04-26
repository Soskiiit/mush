import logging
import os
import time
from pathlib import Path

import Metashape
import adj_django_connection
from catalog.models import Model3D
from django.conf import settings
from django.utils import timezone
from litequeue import LiteQueue
from photogrammetry.tools import json_to_photogrammetry_args


DATABASE_DIR = adj_django_connection.ROOT_DIR / 'db.sqlite3'

photogrammetry_queue = LiteQueue(DATABASE_DIR)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(message)s',
)
handler = logging.FileHandler('photogrammetry.log')
photogrametry_logger = logging.getLogger('photogrammetry_logger')
photogrametry_logger.addHandler(handler)
console_logger = logging.getLogger('console_logger')
console_logger.setLevel(logging.INFO)


def photogrammetry_calc(photo_paths, model_path, model_id):
    try:
        Model3D.objects.filter(id=model_id).update(
            status='in_progress',
            last_update_date=timezone.now()
        )
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
            path=os.path.join(model_path, f'model{model_id}_full.glb')
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
            path=os.path.join(model_path, f'model{model_id}_prev.glb')
        )
        # Normalize path if project runs on Windows
        orig_model_path = os.path.join(
            Path(model_path).parts[-1], f'model{model_id}_full.glb'
        ).replace('\\', '/')
        lowres_model_path = os.path.join(
            Path(model_path).parts[-1], f'model{model_id}_prev.glb'
        ).replace('\\', '/')

        Model3D.objects.filter(id=model_id).update(
            status='completed',
            original=orig_model_path,
            lowres=lowres_model_path,
            face_count=face_count,
            vertex_count=vert_count,
            last_update_date=timezone.now()
        )

    except Exception as ex:
        photogrametry_logger.error(f'{ex} for project with id: {model_id}')
        Model3D.objects.filter(id=model_id).update(
            status='error',
            last_update_date=timezone.now()
        )


if __name__ == '__main__':
    console_logger.info('Waiting for tasks')
    while True:
        if photogrammetry_queue.empty():
            time.sleep(1)
        else:
            try:
                message = photogrammetry_queue.pop().data
                args = json_to_photogrammetry_args(message)
                photogrametry_logger.info(
                    f'starting photogrammetry in project {args["model_id"]}'
                )
                photogrammetry_calc(**args)
                photogrametry_logger.info(
                    f'done photogrammetry in project {args["model_id"]}'
                )
                if photogrammetry_queue.empty():
                    console_logger.info('Waiting for tasks')
            except Exception as ex:
                console_logger.error(
                    f'caught {ex} during photogrammetry process'
                )
                photogrametry_logger.error(
                    f'caught {ex} during photogrammetry process'
                )
