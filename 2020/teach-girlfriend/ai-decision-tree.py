from __future__ import annotations
from typing import List, Tuple

import os
import numpy as np

class DecisionTreeNode:
  """Definition of decision tree node."""
  def __init__(self, values: np.ndarray, labels: np.ndarray, classes: List[int]) -> None:
    """Init tree node with values and classes.

    Args:
      values: array of fit data
      classes: all classes
    """
    self.values = values
    self.labels = labels
    self.classes = classes
    self.info = self.get_info_of(labels)
    self.col_index: int = -1
    self.l, self.r = self.build_children()

  def vote_class_index(self) -> int:
    """Vote the most possible class."""
    return np.argmax(x / self.labels.size \
      for _, x in np.unique(self.labels, return_counts=True))

  def build_children(self) -> Tuple[DecisionTreeNode, DecisionTreeNode]:
    """Build tree with ID3 algorithm."""
    if self.is_leaf(): return None, None
    # calculate the information gain
    n = self.labels.size
    max_info_gain, max_split_col, max_split_point = float('-inf'), -1, float('-inf')
    # 1. for each column, calculate info gain for each point
    for col in range(len(self.values.shape[1])):
      # 2. find each optional split point
      val_range = np.sort(np.unique(self.values[:, col]))
      for split_index in range(len(val_range) - 1):
        # 3. split subset according split point
        split_point = (val_range[split_index] + val_range[split_index + 1]) / 2
        left_set = self.labels[self.values[:, col] < split_point]
        right_set = self.labels[self.values[:, col] > split_point]
        split_info = sum(s.size / n * self.get_info_of(s) for s in [left_set, right_set])
        info_gain = self.info - split_info
        # 4. find max split point with max info gain
        if info_gain > max_info_gain:
          max_info_gain, max_split_col, max_split_point = info_gain, col, split_point
    # 5. build left child and right child with max split point
    left_child_index = self.values[:, max_split_col] < max_split_point
    right_child_index = self.values[:, max_split_col] > max_split_point
    self.col_index, self.split_point = max_split_col, max_split_point
    return (DecisionTreeNode(self.values[idx], self.labels[idx], self.classes) \
      for idx in [left_child_index, right_child_index])

  def get_info_of(self, subset_labels: np.ndarray) -> float:
    """Calculate the info of subset."""
    n = subset_labels.size
    return sum(-x / n * np.log2(x / n) for _, x in np.unique(subset_labels, return_counts=True))

  def is_leaf(self) -> bool:
    """Check if it can not be divided."""
    return not self.values or self.values.size == 0 or np.unique(self.labels[:, -1]).size <= 1

class DecisionTree:
  """Definition of decision tree."""

  def __init__(self, max_depth: int = None) -> None:
    """Init tree with max_depth."""
    self.tree = None
    self.max_depth = max_depth

  def prune(self) -> None:
    """TODO: Prune the tree. """
    pass

  def fit(self, X: np.ndarray, y: np.ndarray) -> None:
    """Fit the decision tree model."""
    assert X.shape[0] == y.shape[0], "X and y should have equal number of elements."
    classes = np.unique(y)
    self.tree = DecisionTreeNode(X, y, classes=classes)

  def predict(self, X: np.ndarray) -> np.ndarray:
    """Predict the classes of the given values."""
    return np.array(self.predict_one_piece(x, self.tree) for x in X)

  def predict_one_piece(self, row_data: np.ndarray, node: DecisionTreeNode) -> int:
    """Predict the class of the specifed data."""
    if not node: return -1
    if not node.l and not node.r: return node.classes[node.class_index]
    return self.predict_one_piece(row_data, node.l if row_data[node.col_index] < node.split_point else node.r)

  @staticmethod
  def load_data(path: str) -> np.ndarray:
    """Load numpy data from file."""
    base_path = os.path.dirname(__file__)
    return np.loadtxt(os.path.join(base_path, path))

if __name__ == '__main__':
  train_data = DecisionTree.load_data('./dataset/ex4-traindata.txt')
  test_data = DecisionTree.load_data('./dataset/ex4-testdata.txt')
  tree = DecisionTree()
  tree.fit(train_data[:, :-1], train_data[:, -1])
  y_pred = tree.predict(test_data[:, :-1])
  print('Acc: {:.2f}'.format(np.sum(y_pred == test_data[:, -1]) / test_data.shape[0]))