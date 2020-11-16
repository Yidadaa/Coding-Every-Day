from __future__ import annotations
from typing import List, Tuple

import os
import numpy as np

class DecisionTreeNode:
  """Definition of decision tree node."""
  def __init__(self, values: np.ndarray, labels: np.ndarray, classes: List[int],
    depth: int = 0, max_depth: int = None) -> None:
    """Init tree node with values and classes.

    Args:
      values: array of fit data
      labels: labels of data
      classes: all classes
      depth: current depth of the node
      max_depth: max depth of tree
    """
    self.values = values
    self.labels = labels
    self.classes = classes
    self.depth = depth
    self.max_depth = max_depth
    self.info = self.get_info_of(labels)
    self.col_index: int = -1
    self.split_point: float = None
    self.l, self.r = self.build_children()
    self.label = self.vote_class()

  def vote_class(self) -> int:
    """Vote the most possible class."""
    labels, label_count = np.unique(self.labels, return_counts=True)
    return labels[np.argmax(label_count)]

  def build_children(self) -> Tuple[DecisionTreeNode, DecisionTreeNode]:
    """Build tree with ID3 algorithm."""
    if self.depth >= self.max_depth or self.is_leaf(): return None, None
    # calculate the information gain
    n = self.labels.size
    max_info_gain, max_split_col, max_split_point = float('-inf'), -1, float('-inf')
    # 1. for each column, calculate info gain for each point
    for col in range(self.values.shape[1]):
      # 2. find each optional split point
      val_range = np.sort(np.unique(self.values[:, col]))
      for split_index in range(len(val_range) - 1):
        # 3. split subset according split point
        split_point = (val_range[split_index] + val_range[split_index + 1]) / 2
        left_set = self.labels[self.values[:, col] < split_point]
        right_set = self.labels[self.values[:, col] > split_point]
        # 4. calculate info of splited subsets
        split_info = sum(s.size / n * self.get_info_of(s) for s in [left_set, right_set])
        info_gain = self.info - split_info
        # 5. find max split point with max info gain
        if info_gain > max_info_gain:
          max_info_gain, max_split_col, max_split_point = info_gain, col, split_point
    # 6. build left child and right child with max split point
    left_child_index = self.values[:, max_split_col] < max_split_point
    right_child_index = self.values[:, max_split_col] > max_split_point
    self.col_index, self.split_point = max_split_col, max_split_point
    return (DecisionTreeNode(self.values[idx], self.labels[idx], self.classes,
      self.depth + 1, self.max_depth) for idx in [left_child_index, right_child_index])

  @staticmethod
  def get_info_of(subset_labels: np.ndarray) -> float:
    """Calculate the info of subset.

    Args:
      subset_labels: a collection of labels

    Return:
      info: info of given subset
    """
    n = subset_labels.size
    return sum(-x / n * np.log2(x / n) for x in np.unique(subset_labels, return_counts=True)[1])

  def is_leaf(self) -> bool:
    """Check if it can not be divided."""
    return self.values is None or self.values.size == 0 or np.unique(self.labels).size <= 1

  def __str__(self) -> str:
    """Override string method."""
    if not self.l and not self.r: return 'class: {}'.format(self.label)
    l_str = 'feature_{} < {}'.format(
      self.col_index, self.split_point) if self.l else ''
    l_info = self.add_tab(str(self.l))
    r_str = 'feature_{} > {}'.format(
      self.col_index, self.split_point) if self.r else ''
    r_info = self.add_tab(str(self.r))
    return '\n'.join([l_str, l_info, r_str, r_info])

  @staticmethod
  def add_tab(s: str) -> str:
    """Add tab to formated string."""
    return '\n'.join([('|   ' if i > 0 else '|-> ') + l for i, l in enumerate(s.split('\n'))])

class DecisionTree:
  """Definition of decision tree."""

  def __init__(self, max_depth: int = 1 << 32, verbose: bool = True) -> None:
    """Init tree with max_depth."""
    self.tree = None
    self.max_depth = max_depth
    self.last_X, self.last_y = None, None
    self.verbose = verbose

  def prune(self, X: np.ndarray = None, y: np.ndarray = None) -> None:
    """Prune the tree with Reduced-Error Pruning (REP). If no (X, y) given, use training data."""
    if X is not None and y is not None and X.size and y.size:
      self.last_X, self.last_y = X, y
    self.do_prune(self.tree)

  def do_prune(self, node: DecisionTreeNode) -> None:
    """Prune the tree."""
    if node is None or (node.l is None and node.r is None): return
    self.do_prune(node.l), self.do_prune(node.r)
    # calculate acc before pruning
    acc_before_prune = self.get_acc_of(self.predict(self.last_X), self.last_y)
    saved_children = (node.l, node.r) # save children
    node.l, node.r = None, None
    # calculate acc after pruning
    acc_after_prune = self.get_acc_of(self.predict(self.last_X), self.last_y)
    if acc_after_prune < acc_before_prune:
      node.l, node.r = saved_children # restore children
    elif self.verbose:
      print('Pruned node: ' + str(saved_children))

  def fit(self, X: np.ndarray, y: np.ndarray) -> None:
    """Fit the decision tree model."""
    assert X.shape[0] == y.shape[0], "X and y should have equal number of elements."
    self.last_X, self.last_y = X, y
    classes = np.unique(y)
    self.tree = DecisionTreeNode(X, y, classes=classes, max_depth=self.max_depth)

  def predict(self, X: np.ndarray) -> np.ndarray:
    """Predict the classes of the given values."""
    return np.array([self.predict_one_piece(x) for x in X])

  def predict_one_piece(self, row_data: np.ndarray) -> float:
    """Predict the class of the specifed data.

    Args:
      row_data: vector of to-be-prediced data

    Return:
      label: predicted label
    """
    node = self.tree
    while node and (node.l or node.r):
      node = node.l if row_data[node.col_index] < node.split_point else node.r
    return node.label if node else -1

  @staticmethod
  def get_acc_of(y_pred: np.ndarray, y: np.ndarray) -> float:
    """Get accurcy of given y_pred and y."""
    return np.sum(y_pred == y) / y.shape[0]

  @staticmethod
  def load_data(path: str) -> Tuple[np.ndarray, np.ndarray]:
    """Load numpy data from file.

    Args:
      path: path of data file

    Returns:
      X: feature of data
      y: label of data
    """
    base_path = os.path.dirname(__file__)
    raw_data = np.loadtxt(os.path.join(base_path, path))
    np.random.shuffle(raw_data)
    return raw_data[:, :-1], raw_data[:, -1]

if __name__ == '__main__':
  np.random.seed(42)
  X_train, y_train = DecisionTree.load_data('./dataset/ex4-traindata.txt')
  X_test, y_test = DecisionTree.load_data('./dataset/ex4-testdata.txt')
  my_tree = DecisionTree()
  my_tree.fit(X_train, y_train)
  my_tree.prune(X_test, y_test)
  my_pred = my_tree.predict(X_test)
  print('\nAcc: {:.2f}'.format(DecisionTree.get_acc_of(my_pred, y_test)))
  print('\nMy Tree:')
  print(my_tree.tree)