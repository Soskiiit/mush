import os
import shutil
from pathlib import Path


def photos_to_model(photos):
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

    metashape_path = (
        '"' + shutil.which('metashape') + '"'
    )  # YOU MUST SPECIFY METASHAPE PATH IN YOUR PATH VARIABLES
    main_script_path = (
        os.path.dirname(os.path.abspath(__file__)) + '/main_script.py'
    )
    model_path = os.path.dirname(os.path.abspath(__file__)) + '/temp/model.glb'
    os.system(
        '{0} -r {1} {2} {3}'.format(
            metashape_path, main_script_path, photo_path, model_path
        )
    )
    print('Photogrammetry done, model saved')
    return model_path
