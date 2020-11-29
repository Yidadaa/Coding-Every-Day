from __future__ import annotations
import functools
import re
from typing import *
import os

import numpy as np
import cv2
import bisect
from tqdm import tqdm
import time

USE_SHAPELY = True

if USE_SHAPELY:
  from shapely.geometry import Polygon, MultiLineString
  from shapely.geometry.linestring import LineString
  from shapely.geometry.polygon import LinearRing

from utils import to_absolute_path

EPS = 0.000001

class KDTree(object):
  """KD-Tree to search points."""
  def __init__(self, points: np.ndarray) -> None:
    self.points = points
    n = self.points.shape[0]
    self.x_sorted = sorted(points[:, 0])
    self.xi_sorted = sorted(range(n), key=functools.cmp_to_key(lambda a, b: points[a][0] - points[b][0]))
    self.y_sorted = sorted(points[:, 1])
    self.yi_sorted = sorted(range(n), key=functools.cmp_to_key(lambda a, b: points[a][1] - points[b][1]))

  def search(self, x_min: float, x_max: float, y_min: float, y_max: float) -> np.ndarray:
    x_l = bisect.bisect_left(self.x_sorted, x_min)
    x_r = bisect.bisect_right(self.x_sorted, x_max)
    y_l = bisect.bisect_left(self.y_sorted, y_min)
    y_r = bisect.bisect_right(self.y_sorted, y_max)
    x_range_indexes = set(self.xi_sorted[x_l:x_r])
    y_range_indexes = set(self.yi_sorted[y_l:y_r])
    selected_points = list(x_range_indexes & y_range_indexes)
    return self.points[selected_points]

class Displayer(object):
  """Display graph."""
  def __init__(self, name: str = 'Polygon', w: int = 720, h: int = 720, ratio: float = 0.8, scale: int = 10) -> None:
    self.img = np.ones((h, w, 3), dtype=np.uint8) * 255
    self.cx, self.cy, self.mw, self.mh = w // 2, h // 2, int(w * ratio), int(h * ratio)
    self.center = np.array([self.cy, self.cy])
    self.name = name
    self.scale = scale

  def draw(self, curves: List[np.ndarray] = [], visibility: List[np.ndarray] = [],
      color: int = 0, ball_radius: int = 0.0, max_d: float = 10) -> None:
    """Draw curves to screen."""
    if curves:
      if len(visibility) == 0: visibility = [None] * len(curves)
      for curve, vis in zip(curves, visibility):
        render_curve = self.xy(curve)
        n = render_curve.shape[0]
        for i in range(n):
          j = (i + 1) % n
          st, ed = render_curve[i], render_curve[j]
          dis = np.linalg.norm(st - ed)
          if dis > self.scale * max_d: continue
          if vis is None or vis[i] and vis[j]:
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

  def __init__(self, curves: List[np.ndarray], norms: List[np.ndarray], visibility: List[np.ndarray] = None, name: str = None) -> None:
    """Init graph with file."""
    self.curves: List[np.ndarray] = curves
    self.norms: List[np.ndarray] = norms
    self.visibility: List[np.ndarray] = self.init_visibility(curves) if visibility is None else visibility
    self.tree: List[int] = self.get_relation()
    self.name = name
    self.all_points = np.concatenate(self.curves) if self.curves else np.array([[0, 0]])
    self.kd_tree = None

  @staticmethod
  def init_visibility(curves: List[np.ndarray]):
    """Initialize visibility for each curve."""
    return [np.ones(c.shape[0]).astype(bool) for c in curves]

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

  def offset(self, d: float, remove: bool = False) -> Graph:
    """Return offset of graph."""
    offset_curves: List[np.ndarray] = []
    offset_all_norms: List[np.ndarray] = []
    offset_all_vis: List[np.ndarray] = []
    if not self.kd_tree: self.kd_tree = KDTree(self.all_points)
    for curve, norm, vis in zip(self.curves, self.norms, self.visibility):
      offset_curve = curve + norm * d
      offset_points = []
      offset_norms = []
      offset_vis = []
      for p, n, v in zip(offset_curve, norm, vis):
        s_points = self.kd_tree.search(p[0] - 2 * d, p[0] + 2 * d, p[1] - 2 * d, p[1] + 2 * d)
        # min_dis = np.linalg.norm(all_points - p, axis=1).min()
        min_dis = np.linalg.norm(s_points - p, axis=1).min()
        if remove and abs(min_dis - d) > EPS: continue
        offset_points.append(p)
        offset_norms.append(n)
        offset_vis.append(v and (abs(min_dis - d) <= EPS))
      if offset_points:
        offset_curves.append(np.array(offset_points))
        offset_all_norms.append(np.array(offset_norms))
        offset_all_vis.append(np.array(offset_vis))
    return Graph(offset_curves, offset_all_norms, offset_all_vis)

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

  @staticmethod
  def norm_of_line(vec: np.ndarray) -> np.ndarray:
    """Get norm of line."""
    norm = np.array([1.0, -vec[0] / (vec[1] + EPS)])
    norm = Graph.normalize(norm)
    norm = norm if np.cross(norm, vec) > 0 else -norm
    return norm

  @staticmethod
  def normalize(vec: np.ndarray) -> np.ndarray:
    l = np.linalg.norm(vec)
    return vec / l if l > EPS else vec

  def interplot(self, max_step: float) -> Graph:
    """Interplot curves with more vertexs."""
    in_curves = []
    in_norms = []
    in_all_vis = []
    for curve, norm, vis in zip(self.curves, self.norms, self.visibility):
      n = curve.shape[0]
      in_curve = []
      in_norm = []
      in_vis = []
      i = 1
      while i < n - 1:
        step_value = np.arccos(np.clip(norm[i - 1].dot(norm[i + 1]) / np.linalg.norm(norm[i - 1]) / np.linalg.norm(norm[i + 1]), -1, 1))
        if step_value <= max_step:
          in_curve.append(curve[i])
          in_norm.append(norm[i])
          in_vis.append(vis[i])
        else:
          interp_count = int(step_value / max_step) + 1
          for si in range(interp_count):
            alpha = 1 - si / interp_count
            # ij_vec, jk_vec = self.norm_of_line(curve[i] - curve[i - 1]), self.norm_of_line(curve[i + 1] - curve[i])
            # in_norm_vec = alpha * ij_vec + (1 - alpha) * jk_vec
            in_norm_vec = alpha * norm[i - 1] + (1 - alpha) * norm[i + 1]
            in_norm.append(self.normalize(in_norm_vec))
            in_curve.append(curve[i])
            in_vis.append(vis[i])
          i += 1
        i += 1
      in_curves.append(np.array(in_curve, dtype=np.float))
      in_norms.append(np.array(in_norm, dtype=np.float))
      in_all_vis.append(np.array(in_vis))
    return Graph(in_curves, in_norms, in_all_vis)

  def interplot_with_distance(self, max_step: float) -> Graph:
    """Interplot graph according to distance."""
    in_curves = []
    in_norms = []
    in_all_vis = []
    for curve, norm, vis in zip(self.curves, self.norms, self.visibility):
      n = curve.shape[0]
      in_curve = []
      in_norm = []
      in_vis = []
      for i in range(n):
        j = (i + 1) % n
        step_value = np.linalg.norm(curve[i] - curve[j])
        in_curve.append(curve[i])
        in_norm.append(norm[i])
        in_vis.append(vis[i])
        if step_value > max_step:
          interp_count = int(step_value / max_step) + 1
          direction_vec = curve[j] - curve[i]
          norm_intp = norm[j] - norm[i]
          for si in range(1, interp_count):
            in_curve.append(curve[i] + si / interp_count * direction_vec)
            in_norm_vec = norm[i] + si / interp_count * norm_intp
            in_norm.append(in_norm_vec / np.linalg.norm(in_norm_vec))
            in_vis.append(vis[i] * vis[j])
      in_curves.append(np.array(in_curve, dtype=np.float))
      in_norms.append(np.array(in_norm, dtype=np.float))
      in_all_vis.append(np.array(in_vis))
    # return Graph(in_curves, [self.get_norms(c) for c in in_curves])
    return Graph(in_curves, in_norms, in_all_vis)

  def zigzag_shadow(self, d: float, resolution: float) -> Tuple[List[np.ndarray], int, float, float]:
    """Generate zig-zag shadow."""
    start_time_point = time.time()
    g = self.interplot_with_distance(resolution).interplot(0.1).offset(d, True).interplot_with_distance(resolution)
    min_y = min(curve[:, 1].min() for curve in self.curves)
    max_y = max(curve[:, 1].max() for curve in self.curves)
    line_count = int((max_y - min_y) / d)
    lines = [i * d + min_y for i in range(line_count + 1)]

    points_group_by_line = [[] for _ in range(line_count + 1)]
    points_group_by_curve = [[] for _ in g.curves]

    intersect_points: List[IntersectPoint] = []
    for ci, curve in enumerate(g.curves):
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
            connected_lines.append((last_point, g.curves[p.curve_index][pi]))
            last_point = g.curves[p.curve_index][pi]
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
    width = min(self.all_points[:, 0].max() - self.all_points[:, 0].min(), self.all_points[:, 1].max() - self.all_points[:, 1].min())
    steps = int(width / d / 2)
    intg = self.interplot_with_distance(resolution)
    lrs = LineString(np.concatenate(intg.curves))
    ret_curves = []
    for i in tqdm(range(steps)):
      next_lrs = []
      ops = lrs.parallel_offset((i + 1) * distance)
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

  def contour_shadow(self, d: float, resolution: float, displayer: Displayer = None, intp_step: int = 1) -> Tuple[List[np.ndarray], float]:
    """Generate contour shadow."""
    start_time_point = time.time()
    width = min(self.all_points[:, 0].max() - self.all_points[:, 0].min(), self.all_points[:, 1].max() - self.all_points[:, 1].min())
    steps = int(width / d / 2)
    g = self.interplot_with_distance(resolution).interplot(0.5)
    curves = [g.curves]

    for i in tqdm(range(steps)):
      g = g.offset(distance, True)
      curves.append(g.interplot_with_distance(resolution).curves)
      # curves += g.curves
      if all(v.sum() == 0 for v in g.visibility): break
      if i % intp_step == 0: g = g.interplot_with_distance(resolution)
    total_time = (time.time() - start_time_point) * 1000
    removed_curves = []
    all_points = np.concatenate([np.concatenate(c) for c in curves])
    for ci in tqdm(range(len(curves) - 1, 0, -1)):
      other_points = np.concatenate([np.concatenate(c) for c in curves[:ci]])
      for c in curves[ci]:
        mask = np.ones(c.shape[0], dtype=bool)
        for pi in range(c.shape[0]):
          dis = np.linalg.norm(other_points - c[pi], axis=1).min()
          mask[pi] = abs(dis - d) < EPS
        removed_curves.append(c[mask])
        # if removed_curves[-1].shape[0] < 10: removed_curves.pop()
    return removed_curves, total_time

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
        norm_vec = Graph.norm_of_line(ik_vec)
      norm_vec = norm_vec / np.linalg.norm(norm_vec)
      norms[j] = norm_vec if np.cross(norm_vec, ik_vec) > 0 else -norm_vec
    norms[-1] = norms[0]
    return norms

  @staticmethod
  def polygon2curves(p: Union['Polygon', LinearRing]) -> List[np.ndarray]:
    """Convert polygon to curves."""
    xy = p.exterior.xy if isinstance(p, Polygon) else p.xy
    return [np.array(list(zip(*xy)))]

if __name__ == '__main__':
  d = Displayer(name='Default', scale=14, w=800, h=800)
  g1 = Graph.from_file(to_absolute_path('./attachments/graph2.csv'))
  d.draw(g1.curves, g1.visibility, ball_radius=0)
  distance = 1
  resolution = 0.1

  (1, 8)
  # g1.contour_shadow_polygon(distance, distance, d)
  # d.draw(g1.offset_simulate(distance * 2))

  l, t = g1.contour_shadow(distance, resolution, d)
  print('Contour total time = {:.2f} ms.'.format(t))
  d.draw(l, color=(255, 0, 0), max_d=distance * 1)

  # zig-zag
  # params = [(0.1, 0.02), (1, 0.1)]
  # lines, count, total_length, total_time = g1.zigzag_shadow(*(params[1]))
  # for st, ed in lines: cv2.line(d.img, tuple(d.xy(st)), tuple(d.xy(ed)), (255, 0, 0))
  # print('Zig-zag with {} horizontal lines, total length = {:.2f} mm, total time = {:.2f}ms.\n'.format(count, total_length, total_time))

  # cv2.imwrite()
  d.show()