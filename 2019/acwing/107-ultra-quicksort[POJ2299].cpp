#include <iostream>

using namespace std;

int a[500010];
int tmp[500010];

long long solve(int n) {
  long long ret = 0;
  for (int step = 1; step < n; step <<= 1) {
    // 开始归并，左闭右开
    for (int l = 0; l < n; l += 2 * step) {
      int m = min(l + step, n); // 对两个指针起点做防越界处理
      int r = min(m + step, n);
      int i = l, j = m;
      for (int t = l; t < r; t += 1) {
        bool cond = (i >= m) || (j < r && a[i] > a[j]); // 当左边值大于右边值时，证明出现了逆序对
        tmp[t] = cond ? a[j++] : a[i++];
        if (cond) ret += m - i;
      }
      for (int i = l; i < r; i++) a[i] = tmp[i];
    }
  }
  return ret;
}

int main() {
  int n = 1;
  cin >> n;
  while (n > 0) {
    for (int i = 0; i < n; i++) cin >> a[i];
    cout << solve(n) << endl;
    cin >> n;
  }
}

// 归并排序求逆序对，非递归实现