"""AIcourse ex3 BP problem"""
from __future__ import annotations
from typing import Tuple
import os, math

import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt


NNGradType = Tuple[np.array, np.array, np.array, np.array]

class LinearNeuralNetwork():
  """Define structure of linear neural network."""

  def __init__(self, input_dim: int, output_dim: int, hidden_units: int, batch_size: int, seed: int = 42) -> None:
    """Init layer with D_i, D_o, H, B, Y = Sigmoid(W_2 * (W_1 * x + b_1) + b2)

    Args:
      input_dim: input dimension
      output_dim: output dimension
      hidden_units: the number of units in hidden layer
      batch_size: batch size
      seed: random seed
    """
    np.random.seed(seed)
    self.input_dim = input_dim
    self.output_dim = output_dim
    self.hidden_units = hidden_units
    self.batch_size = batch_size

    self.w_1 = self.init_params((input_dim, hidden_units))
    self.b_1 = self.init_params((hidden_units, ))
    self.w_2 = self.init_params((hidden_units, output_dim))
    self.b_2 = self.init_params((output_dim, ))

  def forward(self, x: np.array) -> np.array:
    """Forward propagation."""
    assert x.shape[1] == self.input_dim, \
      "Incorrect input dimension {}, which should be {}.".format(x.shape[1], self.input_dim)
    y_pred = (x @ self.w_1 + self.b_1) @ self.w_2 + self.b_2
    return 1 / (1 + np.exp(-y_pred)) # predict with sigmoid

  def backward(self, x: np.array, y_target: np.array) -> Tuple[np.float, NNGradType]:
    """Backward propagation."""
    h = x @ self.w_1 + self.b_1 # shape: n * hidden_units
    y = h @ self.w_2 + self.b_2 # shape: n * out_dim
    sig_y = 1 / (1 + np.exp(-y)) # shape: n * out_dim

    loss = np.square(sig_y - y_target).sum() # shape: 1

    grad_sig_y = 2 * (sig_y - y_target) # shape: n * out_dim
    grad_y = sig_y * (1 - sig_y) * grad_sig_y # shape: n * out_dim
    grad_w_2 = h.T @ grad_y / self.batch_size # shape: hidden_units * out_dim
    grad_b_2 = np.ones(self.batch_size) @ grad_y / self.batch_size # shape: 1 * out_dim
    grad_h = grad_y @ self.w_2.T # shape: n * hidden_units
    grad_w_1 = x.T @ grad_h / self.batch_size # shape: input_dim * hidden_units
    grad_b_1 = np.ones(self.batch_size) @ grad_h / self.batch_size # shape: 1 * hidden_units

    return loss, (grad_w_2, grad_b_2, grad_w_1, grad_b_1)

  def optimize_params(self, grads: NNGradType, lr: float = 0.99):
    """Optimize the parameters of the network."""
    for param_name, grad in zip(['w_2', 'b_2', 'w_1', 'b_1'], grads):
      param = getattr(self, param_name)
      setattr(self, param_name, param - lr * grad)

  def __call__(self, *args):
    """Override callable behavior."""
    return self.forward(*args)

  def init_params(self, shape: Tuple[int, ...]) -> np.array:
    """Init parameters with kaiming init. std = gain / sqrt(fan_mode)."""
    fan_in, gain = shape[0], 1
    return np.random.normal(0, gain / np.sqrt(fan_in), size=shape)


class DataLoader():
  """Iris Dataloader."""

  def __init__(self, train_path: str, test_path: str, seed: int = 42):
    """Load train data and test data.

    Args:
      train_path: the path of train data
      test_path: the path of test data
      seed: random seed
    """
    np.random.seed(seed)
    self.X_train, self.y_train = self.load_data(train_path)
    self.X_test, self.y_test = self.load_data(test_path)

  def load_data(self, file_path: str) -> Tuple[np.array, np.array]:
    """Load data from file."""
    assert os.path.exists(file_path), "File does not exist: {}".format(file_path)
    raw_data = np.loadtxt(file_path)
    np.random.shuffle(raw_data) # shuffle vector randomly
    classes = np.unique(raw_data[:, -1])
    one_hot_labels = np.array([self.to_one_hot(label, classes) for label in raw_data[:, -1]])
    return raw_data[:, :raw_data.shape[1] - 1], one_hot_labels

  def to_one_hot(self, label: float, classes: np.array) -> list:
    """Convert class label to one hot vector."""
    one_hot_vector = np.zeros_like(classes)
    one_hot_vector[classes == label] = 1.0
    return one_hot_vector

  @staticmethod
  def to_abs_path(path: str) -> str:
    """Convert relative path to absolute path."""
    base_path = os.path.dirname(__file__)
    return os.path.join(base_path, path)


class Trainer():
  """Trainer for NN."""

  def __init__(self, data: DataLoader, model: LinearNeuralNetwork, epoch: int = 100, lr: float = 0.99) -> None:
    """Setup trainer."""
    self.data = data
    self.model = model
    self.epoch = epoch
    self.lr = lr

  def train(self, plot_loss: bool = False) -> None:
    """Train the model."""
    losses = []
    with tqdm(total=self.epoch) as t:
      for i in range(self.epoch):
        lr = self.lr * np.cos(i / self.epoch * math.pi / 2)
        loss, grads = self.model.backward(self.data.X_train, self.data.y_train)
        self.model.optimize_params(grads, lr=lr)
        t.set_description('Training {} of {}, loss: {:.4f}'.format(i, self.epoch, loss))
        t.update(1)
        losses.append(loss)
    if plot_loss:
      plt.plot(losses)
      plt.show()

  def test(self) -> None:
    """Test model."""
    y_pred = self.model(self.data.X_test)
    y_pred = np.argmax(y_pred, axis=1)
    y = np.argmax(self.data.y_test, axis=1)
    acc = np.sum(y_pred == y) / self.data.y_test.shape[0]
    print('Acc: {:.4f}'.format(acc))

if __name__ == "__main__":
  train_name, test_name = './dataset/ex3-Iris-train.txt', './dataset/ex3-Iris-test.txt'
  data = DataLoader(DataLoader.to_abs_path(train_name), DataLoader.to_abs_path(test_name))
  model = LinearNeuralNetwork(data.X_train.shape[1], data.y_train.shape[1],
    10, data.X_train.shape[0])
  trainer = Trainer(data, model, epoch=2000, lr=0.8)
  trainer.train(plot_loss=True)
  trainer.test()