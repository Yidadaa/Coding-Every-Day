from numba import cuda
import numpy as np

from time import time

@cuda.jit
def gpu_add(a, b, result, n):
  idx = cuda.threadIdx.x + cuda.blockDim.x * cuda.blockIdx.x
  if idx < n:
    result[idx] = a[idx] / b[idx]

def main():
  n = 10 ** 9
  x = np.arange(n).astype(np.int32)
  y = 2 * x + 0.1

  x_device = cuda.to_device(x)
  y_device = cuda.to_device(y)

  gpu_result = cuda.device_array(n)
  cpu_result = np.empty(n)

  threads_per_block = 1024
  blocks_per_grid = n // 1024 + 1

  print('start adding')
  t = time()
  gpu_add[blocks_per_grid, threads_per_block](x_device, y_device, gpu_result, n)
  cuda.synchronize()

  print('gpu time: ', time() - t)

  t = time()
  cpu_result = x / y
  print('cpu time: ', time() - t)

  if np.array_equal(cpu_result, gpu_result.copy_to_host()):
    print('result correct')

if __name__ == '__main__':
  main()