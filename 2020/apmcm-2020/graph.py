from __future__ import annotations
import functools
from functools import total_ordering
from typing import *
import os

import numpy as np
import cv2
from numpy.linalg.linalg import norm
from shapely.geometry import Polygon, MultiLineString
from shapely.geometry.linestring import LineString
from shapely.geometry.polygon import LinearRing
import bisect
from tqdm import tqdm
import time

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

  def draw(self, curves: List[np.ndarray] = [], color: int = 0, ball_radius: int = 0.0, max_d: float = 1) -> None:
    """Draw curves to screen."""
    if curves:
      for curve in curves:
        render_curve = self.xy(curve)
        n = render_curve.shape[0]
        for i in range(n):
          st, ed = render_curve[i], render_curve[(i + 1) % n]
          dis = np.linalg.norm(curve[i] - curve[(i + 1) % n])
          # if dis > max_d: continue
          cv2.line(self.img, tuple(st), tuple(ed), color=color)
        if ball_radius <= 0: continue
        for i, (x, y) in enumerate(render_curve):
          cv2.circle(self.img, (x, y), int(ball_radius * self.scale), 0, thickness=1)

  def draw_norms(self, g: Graph, width: float = 1) -> None:
    """Draw norm vectors of graph."""
    for curve, norm in zip(g.curves, g.norms):
      for p, n in zip(curve, norm):
        dp = self.xy((p + n * distance * width))
        inp = self.xy(p)
        cv2.line(d.img, tuple(inp), tuple(dp), (0, 168, 0))

  def show(self, delay: int = 0) -> None:
    cv2.imshow(self.name, self.img)
    cv2.waitKey(delay)

  def clear(self) -> None:
    """Clear display."""
    self.img = np.ones_like(self.img) * 255

  def xy(self, pxy: np.ndarray) -> np.ndarray:
    """Get pixel postion of point."""
    return (pxy * self.scale + self.center).astype(np.int)

class IntersectPoint(object):
  def __init__(self, xy: np.ndarray, line_index: int, curve_index: int, st_index: int,
      ed_index: int, mark: int, number_mark: int, lp_index: int) -> None:
    self.xy = xy
    self.line_index = line_index
    self.curve_index = curve_index
    self.st_index = st_index
    self.ed_index = ed_index
    self.mark = mark
    self.number_mark = number_mark
    self.lp_index = lp_index # index in a split line

class Graph(object):
  """Graph object to compute."""

  def __init__(self, curves: List[np.ndarray], norms: List[np.ndarray], name: str = None) -> None:
    """Init graph with file."""
    self.curves: List[np.ndarray] = curves
    self.norms: List[np.ndarray] = norms
    self.tree: List[int] = self.get_relation()
    self.name = name

  def get_relation(self) -> List[int]:
    """Get relationship of each plogon."""
    pass

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
    all_points = np.concatenate(self.curves) if len(self.curves) else []
    for curve, norm in zip(self.curves, self.norms):
      offset_curve = curve + norm * d
      offset_points = []
      for p in offset_curve:
        min_dis = np.linalg.norm(all_points - p, axis=1).min()
        if abs(min_dis - d) > EPS: continue
        offset_points.append(p)
      if offset_points: offset_curves.append(np.array(offset_points))
    return offset_curves

  def offset_simulate(self, d: float) -> list[np.ndarray]:
    """Return offset of graph."""
    points = np.concatenate(self.curves)
    x_min, x_max = points[:, 0].min(), points[:, 0].max()
    y_min, y_max = points[:, 1].min(), points[:, 1].max()
    step = 0.25
    w, h = int((x_max - x_min) / step), int((y_max - y_min) / step)
    curve = []
    for i in range(w):
      for j in range(h):
        x, y = x_min + i * step, y_min + j * step
        p = np.array([x, y])
        dis = np.linalg.norm(points - p, axis=1).min()
        if abs(dis - d) > EPS: continue
        curve.append(p)
    return [np.array(curve)]

  def interplot(self, max_step: float) -> Graph:
    """Interplot curves with more vertexs."""
    in_curves = []
    in_norms = []
    for curve, norm in zip(self.curves, self.norms):
      n = curve.shape[0]
      in_curve = []
      in_norm = []
      i = 1
      while i < n - 1:
        step_value = np.arccos(np.clip(norm[i - 1].dot(norm[i + 1]) / np.linalg.norm(norm[i - 1]) / np.linalg.norm(norm[i + 1]), -1, 1))
        if step_value <= max_step:
          in_curve.append(curve[i])
          in_norm.append(norm[i])
        else:
          interp_count = int(step_value / max_step) + 1
          for si in range(interp_count):
            alpha = 1 - si / interp_count
            in_norm_vec = alpha * norm[i - 1] + (1 - alpha) * norm[i + 1]
            in_norm.append(in_norm_vec / np.linalg.norm(in_norm_vec))
            in_curve.append(curve[i])
          i += 1
        i += 1
      in_curves.append(np.array(in_curve, dtype=np.float))
      in_norms.append(np.array(in_norm, dtype=np.float))
    return Graph(in_curves, in_norms)

  def interplot_with_distance(self, max_step: float) -> Graph:
    """Interplot graph according to distance."""
    in_curves = []
    in_norms = []
    for curve, norm in zip(self.curves, self.norms):
      n = curve.shape[0]
      in_curve = []
      in_norm = []
      for i in range(n):
        j = (i + 1) % n
        step_value = np.linalg.norm(curve[i] - curve[j])
        in_curve.append(curve[i])
        in_norm.append(norm[i])
        if step_value > max_step:
          interp_count = int(step_value / max_step) + 1
          direction_vec = curve[j] - curve[i]
          norm_intp = norm[j] - norm[i]
          for si in range(1, interp_count):
            in_curve.append(curve[i] + si / interp_count * direction_vec)
            in_norm_vec = norm[i] + si / interp_count * norm_intp
            in_norm.append(in_norm_vec / np.linalg.norm(in_norm_vec))
      in_curves.append(np.array(in_curve, dtype=np.float))
      in_norms.append(np.array(in_norm, dtype=np.float))
    # return Graph(in_curves, [self.get_norms(c) for c in in_curves])
    return Graph(in_curves, in_norms)

  def zigzag_shadow(self, d: float) -> Tuple[List[np.ndarray], int, float, float]:
    """Generate zig-zag shadow."""
    start_time_point = time.time()
    curves = self.interplot(0.2).offset(d)
    if d >= 0.5:
      curves = Graph.from_curves(curves).interplot_with_distance(d / 5).curves
    min_y = min(curve[:, 1].min() for curve in self.curves)
    max_y = max(curve[:, 1].max() for curve in self.curves)
    line_count = int((max_y - min_y) / d)
    lines = [i * d + min_y for i in range(line_count + 1)]

    points_group_by_line = [[] for _ in range(line_count + 1)]
    points_group_by_curve = [[] for _ in curves]

    intersect_points: List[IntersectPoint] = []
    for ci, curve in enumerate(curves):
      n = curve.shape[0]
      for i in range(n - 1):
        st, ed = curve[i], curve[i + 1]
        vec = ed - st
        si, ei = self.search_range(lines, st[1], ed[1])
        for li in range(si, ei):
          ly = lines[li]
          int_point = st + (ly - st[1]) / vec[1] * vec
          intp_index = len(intersect_points)
          points_group_by_line[li].append(intp_index)
          points_group_by_curve[ci].append(intp_index)
          # xy, line_index, curve_index, st_index, ed_index, mark, number_mark
          intersect_points.append(IntersectPoint(int_point, li, ci, i, i + 1, None, 2 * li, None))
    for line_index in range(line_count + 1):
      points_group_by_line[line_index].sort(key=functools.cmp_to_key(lambda a, b: intersect_points[a].xy[0] - intersect_points[b].xy[0]))
      for lp_index in range(len(points_group_by_line[line_index])):
        intersect_points[points_group_by_line[line_index][lp_index]].lp_index = lp_index

    # use number mark to connect points
    for layer in points_group_by_curve:
      mark = -1 # initial mark
      for pi in layer:
        p = intersect_points[pi]
        lpi = p.lp_index + (-1 if p.lp_index % 2 else 1) # find adjcent point in the same line
        if lpi < 0 or lpi >= len(points_group_by_line[p.line_index]):
          mark *= -1 # reverse mark
        else:
          np = intersect_points[points_group_by_line[p.line_index][lpi]]
          if np.mark is None or np.mark == mark:
            mark *= -1
        p.mark = mark # mark current point
        p.number_mark += p.mark

    total_length: float = 0.0
    # generate edge lines
    connected_lines: List[np.ndarray] = []
    for layer in points_group_by_curve:
      for lpi in range(len(layer)):
        p, np = intersect_points[layer[lpi]], intersect_points[layer[(lpi + 1) % len(layer)]]
        # we only connect points with equal number mark or the sum of their number marks equals 2 * line_index
        if p.number_mark == np.number_mark or p.line_index == np.line_index \
            and p.number_mark + np.number_mark == 4 * p.line_index:
          last_point = p.xy
          # connect curve between two intersect points
          for pi in range(p.ed_index, np.st_index + 1):
            connected_lines.append((last_point, curves[p.curve_index][pi]))
            last_point = curves[p.curve_index][pi]
          connected_lines.append((last_point, np.xy))
          total_length += self.distance(*connected_lines[-1])

    horizontal_lines_count = len(connected_lines)
    # generate horizontal lines
    for line in points_group_by_line:
      for lpi in range(len(line)):
        if lpi % 2: continue # skip and connect horizontal lines
        p, np = intersect_points[line[lpi]], intersect_points[line[(lpi + 1) % len(line)]]
        connected_lines.append((p.xy, np.xy))
        total_length += self.distance(*connected_lines[-1])
    horizontal_lines_count = len(connected_lines) - horizontal_lines_count
    total_time = (time.time() - start_time_point) * 1000

    return connected_lines, horizontal_lines_count, total_length, total_time

  def contour_shadow_polygon(self, d: float, resolution: float, displayer: Displayer) -> np.ndarray:
    """Generate contour shadow with Shapley."""
    all_points = np.concatenate(self.curves)
    width = min(all_points[:, 0].max() - all_points[:, 0].min(), all_points[:, 1].max() - all_points[:, 1].min())
    steps = int(width / d / 2)
    intg = self.interplot_with_distance(resolution)
    lrs = LineString(np.concatenate(intg.curves))
    ret_curves = []
    for i in tqdm(range(steps)):
      next_lrs = []
      ops = lrs.parallel_offset((i + 1) * distance, resolution=4)
      if isinstance(ops, LineString): ops = [ops]
      for op in ops:
        if op.length < EPS: continue
        xy = op.xy
        if len(xy[0]) < 5: continue
        next_lrs.append(np.array(list(zip(xy[0], xy[1]))))
      if len(next_lrs) == 0: break
      ret_curves += next_lrs
      displayer.draw(next_lrs)
      displayer.show(1)
    return ret_curves

  def contour_shadow(self, d: float, resolution: float, displayer: Displayer) -> List[np.ndarray]:
    """Generate contour shadow."""
    curves = []
    all_points = np.concatenate(self.curves)
    width = min(all_points[:, 0].max() - all_points[:, 0].min(), all_points[:, 1].max() - all_points[:, 1].min())
    steps = int(width / d / 2) + 1
    g = self.interplot(resolution)
    for i in tqdm(range(steps)):
      g = Graph.from_curves(g.offset(distance))
      curves += g.curves
      displayer.draw(g.curves, (255, 0, 0))
      displayer.show(1)
      if i % 1 == 0: g = g.interplot_with_distance(resolution)
    return curves

  @staticmethod
  def distance(st: np.ndarray, ed: np.ndarray) -> float:
    return np.linalg.norm(st - ed)

  @staticmethod
  def search_range(lines: List[float], y_from: float, y_to: float) -> Union[Tuple[int, int], None]:
    """Search y position of line, return a close range [from_index, to_index]."""
    y_from, y_to = min(y_from, y_to), max(y_from, y_to)
    from_index = bisect.bisect_left(lines, y_from)
    to_index = bisect.bisect_right(lines, y_to)
    return (from_index, to_index)

  @staticmethod
  def get_norms(curve: np.ndarray) -> np.ndarray:
    """Get norm vector for each vertex."""
    if curve.shape[0] <= 3: return np.zeros_like(curve)
    n = curve.shape[0] - 1 # trim last point, because the curve is a closed polygon
    norms: np.ndarray = np.zeros_like(curve, dtype=np.float)
    for i in range(n):
      j, k = (i + 1) % n, (i + 2) % n
      ji_vec: np.ndarray = (curve[i] - curve[j])
      jk_vec: np.ndarray = (curve[k] - curve[j])
      ik_vec: np.ndarray = (curve[k] - curve[i])
      norm_vec = ji_vec / (np.linalg.norm(ji_vec) + EPS) + jk_vec / (np.linalg.norm(jk_vec) + EPS)
      if np.linalg.norm(norm_vec) < EPS:
        norm_vec = np.array([1.0, -ik_vec[0] / (ik_vec[1] + EPS)])
      norm_vec = norm_vec / np.linalg.norm(norm_vec)
      norms[j] = norm_vec if np.cross(norm_vec, ik_vec) > 0 else -norm_vec
    norms[-1] = norms[0]
    return norms

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
  d = Displayer(name='Default', scale=14, w=800, h=800)
  g1 = Graph.from_file(to_absolute_path('./attachments/graph1.csv'))
  d.draw(g1.curves, ball_radius=0)
  steps = 5
  distance = 1
  resolution = 0.1

  # g1.contour_shadow_polygon(distance, distance, d)
  # d.draw(g1.offset_simulate(distance * 2))

  # g1.contour_shadow(distance, resolution, d)
  # d.draw_norms(g1)

  # zig-zag
  lines, count, total_length, total_time = g1.zigzag_shadow(distance)
  for st, ed in lines: cv2.line(d.img, tuple(d.xy(st)), tuple(d.xy(ed)), (255, 0, 0))
  print('Zig-zag with {} horizontal lines, total length = {:.2f} mm, total time = {:.2f}ms.\n'.format(count, total_length, total_time))

  d.show()