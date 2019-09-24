#include <iostream>
#include <cstring>

using namespace std;

const int MOD = 9901;

int pow(int p, int x) {
  // 快速幂
  p %= MOD;
  int ret = 1;
  while (x) {
    if (x & 1) ret = ret * p % MOD;
    p = p * p % MOD;
    x >>= 1;
  }
  return ret;
}

int sum(int p, int c) {
  // 求解质因子p的等比数列和
  if (c <= 0) return 1;

  if (c & 1) {
    // c 为奇数个
    return (1 + pow(p, (c + 1) / 2)) * sum(p, (c - 1) / 2) % MOD;
  } else {
    // c 为偶数个
    return (1 + pow(p, c / 2)) * sum(p, c / 2 - 1) % MOD + pow(p, c);
  }
}

int main() {
  int A, B;
  cin >> A >> B;

  int ret = 1;
  for (int i = 2; i <= A; i++) {
    int count = 0;
    while (A % i == 0) {
      count ++;
      A /= i;
    }
    if (count) ret = ret * sum(i, count * B) % MOD;
  }

  if (A == 0) ret = 0;
  cout << ret << endl;

  return 0;
}