from __future__ import annotations
from typing import *
import os


def to_absolute_path(relative_path: str) -> str:
  """Convert relateive path to absolute path."""
  base_path = os.path.dirname(__file__)
  return os.path.join(base_path, relative_path)
