import random
from tqdm import tqdm

n = 200000
w = 1000000
ord_a = ord('a')

def random_string():
  s, l = '', random.randint(1, 200)
  for i in range(l):
    s += chr(ord_a + random.randint(0, 25))
  return s

with open('o.in2', 'w') as f:
  f.write(f'{n}\n')
  for i in tqdm(range(n)):
    s = random_string()
    f.write(f'{s} {w}\n')
  f.write(f'{n}\n')
  for i in tqdm(range(n)):
    s = random_string()
    f.write(f'{s} {w}\n')