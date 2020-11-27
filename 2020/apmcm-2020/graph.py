from __future__ import annotations
from logging import disable
from os import curdir, stat
from typing import *
import os
from matplotlib.pyplot import sca

import numpy as np
import cv2
from numpy.lib.arraysetops import isin
from shapely.geometry import Polygon, MultiPolygon, JOIN_STYLE, CAP_STYLE
from shapely.geometry.point import Point
from shapely.geometry.polygon import LinearRing
import bisect

from utils import to_absolute_path

EPS = 0.000001

class Displayer(object):
  """Display graph."""
  def __init__(self, name: str = 'Polygon', w: int = 720, h: int = 720, ratio: float = 0.8, scale: int = 10) -> None:
    self.img = np.ones((h, w, 3), dtype=np.uint8) * 255
    self.cx, self.cy, self.mw, self.mh = w // 2, h // 2, int(w * ratio), int(h * ratio)
    self.center = np.array([self.cy, self.cy])
    self.name = name
    self.scale = scale

  def draw(self, curves: list[np.ndarray] = [], color: int = 0, ball_radius: int = 0.0) -> None:
    """Draw curves to screen."""
    if curves:
      for curve in curves:
        render_curve = self.xy(curve)
        cv2.polylines(self.img, [render_curve], isClosed=True, color=color)
        if ball_radius <= 0: continue
        for x, y in render_curve:
          cv2.circle(self.img, (x, y), int(ball_radius * self.scale), 0, thickness=1)

  def show(self) -> None:
    cv2.imshow(self.name, self.img)
    cv2.waitKey()

  def clear(self) -> None:
    """Clear display."""
    self.img = np.ones_like(self.img) * 255

  def xy(self, pxy: np.ndarray) -> np.ndarray:
    """Get pixel postion of point."""
    return (pxy * self.scale + self.center).astype(np.int)

class Graph(object):
  """Graph object to compute."""

  def __init__(self, curves: List[np.ndarray], norms: List[np.ndarray], name: str = None) -> None:
    """Init graph with file."""
    self.curves: List[np.ndarray] = curves
    self.norms: List[np.ndarray] = norms
    self.name = name

  @staticmethod
  def from_file(file_path: str) -> Graph:
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
    g = Graph.from_curves([np.array(curve) for curve in curves])
    g.name = os.path.basename(file_path)
    return g

  @staticmethod
  def from_curves(curves: List[np.ndarray]) -> Graph:
    """Build graph from curves."""
    norms = [Graph.get_norms(curve) for curve in curves]
    return Graph(curves, norms)

  def offset(self, d: float) -> list[np.ndarray]:
    """Return offset of graph."""
    offset_curves: List[np.ndarray] = []
    for curve, norm in zip(self.curves, self.norms):
      offset_curve = curve + norm * d
      offset_points = []
      for p in offset_curve:
        min_dis = min(np.linalg.norm(curve - p, axis=1).min() for curve in self.curves)
        if abs(min_dis - d) > EPS:
          continue
        offset_points.append(p)
      if offset_points: offset_curves.append(np.array(offset_points))
    return offset_curves

  def interplot(self, max_step: float) -> Graph:
    """Interplot curves with more vertexs."""
    in_curves = []
    in_norms = []
    for curve, norm in zip(self.curves, self.norms):
      n = curve.shape[0]
      in_curve = []
      in_norm = []
      for i in range(n - 1):
        angle = np.arccos(norm[i].dot(norm[i + 1]) / np.linalg.norm(norm[i]) / np.linalg.norm(norm[i + 1]))
        in_curve.append(curve[i])
        in_norm.append(norm[i])
        if angle > max_step:
          interp_count = int(angle / max_step) + 1
          direction_vec = curve[i + 1] - curve[i]
          norm_intp = norm[i + 1] - norm[i]
          for si in range(1, interp_count):
            in_curve.append(curve[i] + si / interp_count * direction_vec)
            in_norm_vec = norm[i] + si / interp_count * norm_intp
            in_norm.append(in_norm_vec / np.linalg.norm(in_norm_vec))
      in_curves.append(np.array(in_curve, dtype=np.float))
      in_norms.append(np.array(in_norm, dtype=np.float))
    return Graph(in_curves, in_norms)

  def zigzag_shadow(self, d: float) -> np.ndarray:
    """Generate zig-zag shadow."""
    c = self.offset(d)
    min_y = min(curve[:, 1].min() for curve in c)
    max_y = max(curve[:, 1].max() for curve in c)
    line_count = int((max_y - min_y) / d)
    lines = [i * d + min_y for i in range(line_count + 1)]
    sorted_points_along_line = [[] for i in range(line_count + 1)]
    intersect_points: List[np.ndarray] = []
    for curve in self.curves:
      n = curve.shape[0]
      for i in range(n - 1):
        st, ed = curve[i], curve[i + 1]
        vec = ed - st
        si, ei = self.search_range(lines, st[1], ed[1])
        for li in range(si, ei):
          ly = lines[li]
          sorted_points_along_line[li].append(len(intersect_points))
          intersect_points.append(st + (ly - st[1]) / vec[1] * vec)
    return intersect_points, sorted_points_along_line, lines

  @staticmethod
  def search_range(lines: List[float], y_from: float, y_to: float) -> Union[Tuple[int, int], None]:
    """Search y position of line, return a close range [from_index, to_index]."""
    y_from, y_to = min(y_from, y_to), max(y_from, y_to)
    from_index = bisect.bisect_left(lines, y_from)
    to_index = bisect.bisect_right(lines, y_to)
    return (from_index, to_index)

  @staticmethod
  def get_norms(curve: np.ndarray, step: int = 0) -> np.ndarray:
    """Get norm vector for each vertex."""
    if curve.shape[0] <= 3: return np.array()
    n = curve.shape[0] - 1 # trim last point, because the curve is a closed polygon
    norms: np.ndarray = np.zeros_like(curve, dtype=np.float)
    for i in range(n):
      j, k = (i + 1) % n, (i + 2) % n
      ji_vec: np.ndarray = (curve[i] - curve[j])
      jk_vec: np.ndarray = (curve[k] - curve[j])
      ik_vec: np.ndarray = (curve[k] - curve[i])
      norm_vec = ji_vec / np.linalg.norm(ji_vec) + jk_vec / np.linalg.norm(jk_vec)
      if np.linalg.norm(norm_vec) > EPS: norm_vec = norm_vec / np.linalg.norm(norm_vec)
      norms[j] = norm_vec if np.cross(norm_vec, ik_vec) > 0 else -norm_vec
    norms[-1] = norms[0]
    # avg filter over norms
    if step == 0: return norms
    conv_norm = np.zeros_like(norms)
    for i in range(n - step):
      conv_norm[i] = np.mean(norms[i:i + step], axis=0)
      conv_norm[i] /= np.linalg.norm(conv_norm[i])
    return conv_norm

  @staticmethod
  def polygon2curves(p: Union[Polygon, LinearRing]) -> list[np.ndarray]:
    """Convert polygon to curves."""
    xy = p.exterior.xy if isinstance(p, Polygon) else p.xy
    return [np.array(list(zip(*xy)))]

def test_graph():
  curve = np.array([[0, 0], [0, 1], [1, 0], [0, 0]], dtype=np.float)
  norms = Graph.get_norms(curve)
  # print(norms)

if __name__ == '__main__':
  test_graph()
  d = Displayer(name='Default', scale=10)
  g1 = Graph.from_file(to_absolute_path('./attachments/graph1.csv'))
  d.draw(g1.curves, ball_radius=0)
  steps = 20
  distance = 0.5
  # g1 = g1.interplot(0.5)
  # print(g1.curves[0].shape)
  # for i in range(steps):
  #   # draw_g = Graph.from_curves(draw_g.offset(distance))
  #   # d.draw(draw_g.curves, color=(0, 255, 0))
  #   d.draw(g1.offset(distance * (i + 1)), color=(255, 0, 0))

  center = np.array([d.cx, d.cy])
  # for p, n in zip(g1.curves[0], g1.norms[0]):
  #   dp = ((p + n * distance) * d.scale).astype(np.int) + center
  #   inp = (p * d.scale).astype(np.int) + center
  #   cv2.line(d.img, tuple(inp), tuple(dp), (0, 168, 0))
  offset_g1 = Graph.from_curves(g1.offset(distance))
  points, slps, lines = offset_g1.zigzag_shadow(distance)
  count = 0
  for pi in range(len(points) - 1):
    # cv2.circle(d.img, tuple((points[pi] * d.scale).astype(np.int) + center), 0.1, (255, 0, 0), -1)
    st, ed = points[pi], points[pi + 1]
    count += int(abs(st[1] - ed[1]) > EPS)
    if count % 2 == 0: continue
    cv2.line(d.img, tuple(d.xy(st)), tuple(d.xy(ed)), (255, 0, 0))

  for slp, line in zip(slps, lines):
    for i in range(0, len(slp), 2):
      st, ed = points[slp[i]], points[slp[i + 1]]
      cv2.line(d.img, tuple(d.xy(st)), tuple(d.xy(ed)), (255, 0, 0))
  d.show()