from PIL import Image
import numpy as np
import logging as log
import sys
import os
import argparse

from voxelfuse.voxel_model import VoxelModel
from voxelfuse.mesh import Mesh
from voxelfuse.primitives import generateMaterials

log.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s - %(message)s', stream=sys.stdout, level=log.INFO)

def open_images(path):
    log.info(f'loading images from path=`{path}`')
    filenames = []
    for file in os.listdir(path):
        if file.endswith('.png'):
            filenames.append(os.path.join(path, file))
    log.info(f'Found {len(filenames)} images')

    images = [np.array(Image.open(i)) for i in filenames]
    images = np.dstack(images)
    images[images == 255] = 1
    log.info(f'loaded, shape={images.shape}')
    return images

def to_stl_object(images, output_file):
    # https://3dprinting.stackexchange.com/questions/10205/convert-a-3d-numpy-array-of-voxels-to-an-stl-file (accessed 30th October 2022)
    model = VoxelModel(images, generateMaterials(4))  #4 is aluminium.
    mesh = Mesh.fromVoxelModel(model)
    mesh.export(output_file)
    log.info(f'exported to `{output_file}`')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', help='Folder for images, loads all ending in .png', required=True)
    parser.add_argument('-o', '--output_file', help='Name of stl file', required=True)
    args = parser.parse_args()

    images = open_images(args.folder)
    to_stl_object(images, args.output_file)

if __name__ == '__main__':
    main()