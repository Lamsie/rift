from typing import Optional, Collection, Callable

from PIL import Image as PIL_Image, ImageFilter as PIL_ImageFilter


__all__ = [
    'draw_on_image',
]


def draw_on_image(back_image: PIL_Image.Image, front_image_factory: Callable[..., PIL_Image.Image],
                  front_image_filters: Optional[Collection[PIL_ImageFilter.Filter]] = None,
                  **kwargs) -> PIL_Image.Image:
    size = back_image.size
    front_image = front_image_factory(size, **kwargs)
    if front_image_filters is not None:
        for filter_ in front_image_filters:
            front_image = front_image.filter(filter_)
    img = PIL_Image.alpha_composite(back_image, front_image)
    return img

