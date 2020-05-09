import math
import random

from typing import Tuple, Optional, Collection

from PIL import Image as PIL_Image, ImageDraw as PIL_ImageDraw, ImageFilter as PIL_ImageFilter

from .common import draw_on_image


__all__ = [
    'get_stains_image',
    'draw_stains',
]


def get_stains_image(size: Tuple[int, int], rgba_color: Tuple[int, int, int, int], d: int = 10,
                     d_scatter: int = 0, count: int = 10) -> PIL_Image.Image:
    assert len(size) == 2
    assert size[0] > 0 and size[1] > 0
    assert len([c for c in rgba_color if 0 <= c < 256]) == 4
    assert d > 0
    assert d_scatter >= 0
    assert count > 0

    img = PIL_Image.new('RGBA', size)
    ctx = PIL_ImageDraw.Draw(img)
    for _ in range(count):
        x0, y0 = random.randrange(-1 * d, size[0]), random.randrange(-1 * d, size[1])
        x1, y1 = x0 + d, y0 + d
        if d_scatter:
            x1 += random.randint(0, d_scatter)
            y1 += random.randint(0, d_scatter)
        ellipse_bb_coords = [(x0, y0), (x1, y1)]
        ctx.ellipse(ellipse_bb_coords, fill=rgba_color)
    return img


def draw_stains(img: PIL_Image.Image,
                stains_image_filters: Optional[Collection[PIL_ImageFilter.Filter]] = None,
                **kwargs) -> PIL_Image.Image:
    """Return stained image."""
    return draw_on_image(img, get_stains_image, stains_image_filters, **kwargs)

