import math
import random

import numpy as np
import matplotlib.pyplot as plt

from typing import Tuple, Optional, Collection

from scipy.stats import bernoulli
from PIL import Image as PIL_Image, ImageFilter as PIL_ImageFilter

from .common import draw_on_image


__all__ = [
    'get_cracks',
    'plot_cracks',
    'get_cracks_image',
    'draw_cracks',
]


def get_cracks(size: Tuple[int, int], *, simple_fork: bool = True, **kwargs) -> Tuple[np.ndarray, float]:
    assert len(size) == 2
    assert size[0] > 0 and size[1] > 0

    mtx = np.zeros(size, dtype=np.uint8)

    def stain(x_: float, y_: float) -> None:
        x_, y_ = int(x_), int(y_)
        x_ = abs(x_) % size[0]
        y_ = abs(y_) % size[1]
        mtx[x_, y_] = 1

    # Draw a crack and return its length
    def crack(x_: float, y_: float, angle: float, angle_amp: float = math.pi / 6, angle_dist: float = 10.0,
              fork_dist: float = 100.0, end_dist: float = 1000.0, end_dist_factor: float = 0.1,
              exact_end_dist: Optional[int] = None, exact_end_fork_factor: float = 0.25, step: float = 1.0) -> float:
        dist: float = 0.0
        forks_length: float = 0.0
        while True:
            angle_p = math.exp(-1 * dist / angle_dist)
            fork_p = math.exp(-1 * dist / fork_dist)
            end_p = math.exp(-1 * dist / end_dist)
            
            # Decide either to end the crack or not
            if exact_end_dist is None:
                # End the crack with probability (1 - end_p)
                if bernoulli.rvs(1 - end_p):
                    break
            else:
                if dist + forks_length > exact_end_dist:
                    break
            
            # Decide either to fork the crack or not
            if bernoulli.rvs(1 - fork_p):
                if simple_fork:
                    # Fork a new crack perpendicularly
                    cc_angle = angle + random.choice([-1, 1]) * math.pi / 2
                else:
                    # Fork a new crack in a different direction and
                    # alter the current crack's propagation angle too
                    angle_delta = random.uniform(-1, 1) * angle_amp
                    angle = angle + angle_delta
                    cc_angle = angle - angle_delta
                cc_end_dist = end_dist * end_dist_factor
                cc_exact_end_dist = (None
                                     if exact_end_dist is None else
                                     (exact_end_dist - dist - forks_length) * exact_end_fork_factor)
                forks_length += crack(x_, y_, angle=cc_angle, end_dist=cc_end_dist, exact_end_dist=cc_exact_end_dist)
            
            # Changes angle of the crack propagation with probability of (1 - angle_p)
            if bernoulli.rvs(1 - angle_p):
                angle += random.uniform(-1, 1) * angle_amp
            
            x_ += step * math.cos(angle)
            y_ += step * math.sin(angle)
            dist += step
            stain(x_, y_)
        return dist + forks_length
    
    x = random.randrange(0, size[0])
    y = random.randrange(0, size[1])
    angle = 2 * math.pi * random.random()
    length = crack(x, y, angle, **kwargs)
    return mtx, length


def plot_cracks(nrows_: int = 5, ncols_: int = 5, figsize: Tuple[int, int] = (12, 12), **kwargs) -> None:
    assert nrows_ > 1 and ncols_ > 1
    _, axes = plt.subplots(nrows=nrows_, ncols=ncols_, sharex=True, sharey=True, figsize=figsize)
    for i in range(nrows_):
        for j in range(ncols_):
            m, l = get_cracks((100, 100), **kwargs)
            plt.sca(ax=axes[i][j])
            plt.title(f'{l:.2f}')
            plt.imshow(m)


def get_cracks_image(size: Tuple[int, int], crack_width: float = 1.0,
                     filling_ratio: Optional[float] = None,
                     **kwargs) -> PIL_Image.Image:
    source_size = [int(s / crack_width) for s in size]
    if filling_ratio is not None:
        # exact_end_dist correlates with the area occupied by the crack
        kwargs['exact_end_dist'] = filling_ratio * source_size[0] * source_size[1]
    mtx, _ = get_cracks(source_size, **kwargs)
    mtx *= 255
    rgba_mtx = np.array([mtx for _ in range(4)]).transpose(1, 2, 0)
    img = PIL_Image.fromarray(rgba_mtx, mode='RGBA').resize(size)
    return img


def draw_cracks(img: PIL_Image.Image,
                cracks_image_filters: Optional[Collection[PIL_ImageFilter.Filter]] = None,
                **kwargs) -> PIL_Image.Image:
    """Return image with cracks."""
    return draw_on_image(img, get_cracks_image, cracks_image_filters, **kwargs)

