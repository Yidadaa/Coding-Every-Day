import random

def main():
  n = 10000
  max_n = 1000
  win_count = 0

  for i in range(n):
    for j in range(max_n):
      c = random.random() > 0.5
      if c:
        win_count += j % 2 == 0
        break
  print(win_count, n)


if __name__ == '__main__':
  main()