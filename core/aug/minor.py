import random

from typing import Dict, Any

from PIL import Image as PIL_Image

from .cracks import draw_cracks
from .stains import draw_stains


__all__= [
    'to_sepia',
    'lower_contrast_old_style',
    'age'
]


_sepia_ccmtx = [
    0.393, 0.769, 0.189, 0,
    0.349, 0.686, 0.168, 0,
    0.272, 0.564, 0.131, 0,
]


def to_sepia(img: PIL_Image.Image, scatter: bool = True) -> PIL_Image.Image:
    """Alter color palette of an image to make it look old."""
    ccmtx = [x + random.uniform(-0.01, 0.01) for x in _sepia_ccmtx]
    img = img.convert('RGB', ccmtx)
    return img


def lower_contrast_old_style(img: PIL_Image.Image) -> PIL_Image.Image:
    """Lower contrast of an image to make it look old."""
    value = 0.55 + random.uniform(-0.5, 0.5) * 0.1
    img = PIL_ImageEnhance.Contrast(img).enhance(value)
    return img


def age(img, stains_kwargs: Dict[str, Any] = {}, cracks_kwargs: Dict[str, Any] = {}):
    img = to_sepia(img)

    img = img.convert('RGBA')
    c = random.randrange(0, 256)
    rgb = [c for _ in range(3)]
    img = draw_stains(img, rgba_color=(*rgb, 32), **stains_kwargs)
    img = draw_cracks(img, **cracks_kwargs)
    img = img.convert('RGB')

    img = lower_contrast_old_style(img)
    return img

