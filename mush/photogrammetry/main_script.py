import os
import sys

import Metashape

photo_path = sys.argv[1]
model_path = sys.argv[2]
photos = [os.path.join(photo_path, cur_photo) for cur_photo in os.listdir(photo_path)]

print('loaded photos:', photos)

doc = Metashape.app.document
chunk = doc.addChunk()
chunk.addPhotos(photos)
chunk.matchPhotos(downscale=1, generic_preselection=True, reference_preselection=False)
chunk.alignCameras()
chunk.buildDepthMaps(downscale=4, filter_mode=Metashape.AggressiveFiltering)
chunk.buildModel(
    source_data=Metashape.DepthMapsData,
    surface_type=Metashape.Arbitrary,
    interpolation=Metashape.EnabledInterpolation,
)
chunk.buildUV(mapping_mode=Metashape.GenericMapping)
chunk.buildTexture(blending_mode=Metashape.MosaicBlending, texture_size=4096)
chunk.exportModel(path=model_path)
