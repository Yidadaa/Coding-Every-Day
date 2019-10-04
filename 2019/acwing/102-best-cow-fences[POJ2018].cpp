#include <iostream>

using namespace std;

const int MAX = 1e5 + 1;
double a[MAX], b[MAX], s[MAX];

int main() {
  int N, F;
  cin >> N >> F;
  
  double max_a = MAX, min_a = 0;
  for (int i = 1; i <= N; i++) {
    cin >> a[i];
    max_a = max(max_a, a[i]);
    min_a = min(min_a, a[i]);
  }
  
  double eps = 1e-5, l = min_a, r = max_a;
  while (r - l > eps) {
    double m = (l + r) / 2;
    // 减去当前均值
    for (int i = 1; i <= N; i++) b[i] = a[i] - m;
    // 求前缀和
    for (int i = 1; i <= N; i++) s[i] = s[i - 1] + b[i];
    // 判断是否合法
    double max_sum = -1e10, min_s = 1e10;
    for (int i = F; i <= N; i++) {
      min_s = min(min_s, s[i - F]);
      max_sum = max(max_sum, s[i] - min_s);
    }
    if (max_sum >= 0) l = m;
    else r = m;
  }
  
  cout << int(r * 1000) << endl;
}

// 综合题：二分搜索 + 前缀和