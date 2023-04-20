from pygltflib import GLTF2


class GLTFMetadata:
    def __init__(self, fc=0, vc=0) -> None:
        self.face_count, self.vertex_count = fc, vc


def get_gltf_metadata(gltf_path: str) -> GLTFMetadata:
    gltf = GLTF2().load(gltf_path)
    meta = GLTFMetadata()

    for mesh in gltf.meshes:
        meta.vertex_count += sum(
            gltf.accessors[primitive.attributes.POSITION].count
            for primitive in mesh.primitives
        )

    # It is possible to count faces but it's tricky
    # Reference: https://pypi.org/project/pygltflib
    meta.face_count = 0

    return meta
