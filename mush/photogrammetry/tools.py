import os
import threading
from pathlib import Path

from catalog.models import Photo, Project
from django.conf import settings

if settings.ENABLE_PHOTOGRAMMETRY:
    import Metashape


def photogrammetry_main_thread(photo_paths, model_path, project_id):
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
        chunk.buildUV(mapping_mode=Metashape.GenericMapping)
        chunk.buildTexture(
            blending_mode=Metashape.MosaicBlending, texture_size=4096
        )
        chunk.smoothModel()
        chunk.exportModel(
            path=os.path.join(model_path, f'model{project_id}_full.glb')
        )

        chunk.decimateModel(face_count=settings.LOWRES_MODEL_FACE_COUNT)
        chunk.buildUV(mapping_mode=Metashape.GenericMapping, texture_size=2048)
        chunk.buildTexture(
            blending_mode=Metashape.MosaicBlending, texture_size=1024
        )
        chunk.exportModel(
            path=os.path.join(model_path, f'model{project_id}_prev.glb')
        )
        Project.objects.filter(id=project_id).update(
            status='completed', model_lod='/'.join(Path(model_path).parts[-2:])
        )
    except Exception as ex:
        print(ex)
        Project.objects.filter(id=project_id).update(status='error')


def run_photogrammetry_thread(project_id):
    if not settings.ENABLE_PHOTOGRAMMETRY:
        return None
    photo_paths = Photo.objects.filter(for_project_id=project_id).values_list(
        'image', flat=True
    )
    photo_paths = [
        f'{settings.MEDIA_ROOT}/{cur_photo_path}'
        for cur_photo_path in photo_paths
    ]
    
    # Для удобного тестирования - импорт фоток из глобальной папки
    # photo_path = 'D:\Media\Photos\Photogram\examples\Meshroom_6_monstree'

    # photo_paths = [
    #     os.path.join(photo_path, cur_photo)
    #     for cur_photo in os.listdir(photo_path)
    # ]

    model_path = os.path.join(settings.MEDIA_ROOT, 'models')
    photogrammetry_thread = threading.Thread(
        target=photogrammetry_main_thread,
        args=(photo_paths, model_path, project_id),
    )
    Project.objects.filter(id=project_id).update(status='in_progress')
    photogrammetry_thread.start()

    return model_path
