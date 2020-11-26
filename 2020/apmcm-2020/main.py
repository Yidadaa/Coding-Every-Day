from __future__ import annotations
from typing import *

from shapely.geometry import Polygon

from graph import Graph

if __name__ == '__main__':
  g1 = Graph('./attachments/graph1.csv')
  g1.display()
  g2 = Graph('./attachments/graph2.csv')
  g2.display()