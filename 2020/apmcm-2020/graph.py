from __future__ import annotations
from typing import *
import os

import numpy as np
import cv2
from shapely.geometry import Polygon

from utils import to_absolute_path


class Graph(object):
  """Graph object to compute."""

  def __init__(self, file_path: str) -> None:
    """Init graph with file."""
    self.curves: List[np.ndarray] = self.load_graph(to_absolute_path(file_path))
    self.file_name = os.path.basename(file_path)

  def load_graph(self, file_path: str) -> List[np.ndarray]:
    """Load graph from file."""
    assert os.path.exists(file_path), "Graph file not exists: {}".format(file_path)
    with open(file_path, 'r') as f:
      raw_content = f.read()
      raw_lines = raw_content.split('\n')[1:]
      curves = []
      for line in raw_lines:
        if line == 'X,Y' or len(line) == 0: continue
        if 'MainCurve' in line:
          curves.append([])
        else:
          curves[-1].append(list(map(float, line.split(','))))
    return [np.array(curve) for curve in curves]

  def display(self, w: int = 1280, h: int = 720, ratio: float = 0.8) -> None:
    """Display ploygon."""
    img = np.ones((h, w), dtype=np.uint8) * 255
    cx, cy, mw, mh = w // 2, h // 2, int(w * ratio), int(h * ratio)
    max_x = max(curve[:, 0].max() for curve in self.curves)
    min_x = min(curve[:, 0].min() for curve in self.curves)
    max_y = max(curve[:, 1].max() for curve in self.curves)
    min_y = min(curve[:, 1].min() for curve in self.curves)
    # scale point to render area coord
    for curve in self.curves:
      render_curve: np.ndarray = curve.copy()
      render_curve[:, 0] = render_curve[:, 0] / abs(max_x - min_x) * mw + cx
      render_curve[:, 1] = render_curve[:, 1] / abs(max_y - min_y) * mh + cy
      render_curve = render_curve.astype(np.int)
      cv2.polylines(img, [render_curve], isClosed=True, color=0)
    cv2.imshow(self.file_name, img)
    cv2.waitKey()


if __name__ == '__main__':
  g1 = Graph('./attachments/graph1.csv')
  g1.display()
  p = Polygon(g1.curves[0])
  print('')