import numpy as np


def semicircle_path(left_end, right_end, N=100):
    t = np.linspace(0, np.pi, N)
    center = (left_end + right_end) / 2
    radius = (right_end - left_end) / 2
    x = center + radius * np.cos(t)
    y = radius * np.sin(t)
    path = f'M {x[0]}, {y[0]}'
    for k in range(1, len(t)):
        path += f'L{x[k]}, {y[k]}'
    return path
