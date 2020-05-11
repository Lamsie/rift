#!../venv/bin/python3
import sys
sys.path.append('../')

import functools
import click

from pathlib import Path

from joblib import Parallel, delayed
from PIL import Image, ImageFilter
from tqdm import tqdm

from core.aug.minor import age


stains_kwargs = {
    'stains_image_filters': [ImageFilter.GaussianBlur(2)],
    'd': 25,
    'd_scatter': 10,
    'count': 10,
}

cracks_kwargs = {
    'cracks_image_filters': [
        ImageFilter.GaussianBlur(radius=1.6),
        ImageFilter.EDGE_ENHANCE_MORE,
    ],
    'crack_width': 2.0,
    'filling_ratio': 0.05,
    'angle_dist': 500,
    'fork_dist': 10000,
}

age = functools.partial(age, stains_kwargs=stains_kwargs, cracks_kwargs=cracks_kwargs)
dir_type = functools.partial(click.Path, file_okay=False, dir_okay=True, writable=True, readable=True, 
                             resolve_path=False, allow_dash=False, path_type=str)


@click.command()
@click.option('--dataset-path', type=dir_type(exists=True), default='../datasets/lfw',
              show_default=True, help='LFW Dataset root')
@click.option('--dest-path', type=dir_type(exists=False), default='../datasets/lfw_rearranged', 
              show_default=True, help='Path to a directory in which the rearranged dataset will be stored')
def preprocess(dataset_path, dest_path):
    """Preprocess LFW Dataset."""
    dataset_path = Path(dataset_path)
    dest_path = Path(dest_path)
    dest_path.mkdir(parents=True, exist_ok=True)
    gt_path = (dest_path / 'gt')
    gt_path.mkdir(parents=True, exist_ok=True)
    aged_path = (dest_path / 'aged')
    aged_path.mkdir(parents=True, exist_ok=True)
    
    def _preprocess(i, p):
        name_ = f'{i:08}.jpg'
        img = Image.open(p)
        img.save(gt_path / name_)
        img = age(img)
        img.save(aged_path / name_)
        return name_    
    
    images = list(dataset_path.glob('**/*.jpg'))
    Parallel(n_jobs=-1)(delayed(_preprocess)(i, p) for i, p in enumerate(tqdm(images)))


if __name__ == '__main__':
    preprocess()

