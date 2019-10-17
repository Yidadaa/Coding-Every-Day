#include <iostream>
#include <algorithm>

using namespace std;

int a[500010];
int tmp[500010];
int n, m;
long long t;

int merge_sort(int l, int m, int r) {

}

int solve() {
  int cnt = 0;
  for (int l = 0, r = 0; l < n; l = r) {
    int step = 1, should_sort = 1;
    while (step > 0) {
      long long sum = 0;
      if (r + step <= n) {
        if (should_sort) {
          for (int i = l; i < r + step; i ++) tmp[i] = a[i];
          sort(a + l, a + r + step);
        }

        int i = l, j = r + step - 1;
        for (int t = 0; t < m && i < j; t ++, i ++, j --) {
          sum += (a[i] - a[j]) * (a[i] - a[j]);
        }

        if (sum <= t) // 如果需要扩展，则将数组复原
          for (int i = l; i < r + step; i ++) a[i] = tmp[i];
        else // 否则只复原新增部分数组
          for (int i = r + step / 2; i < r + step; i ++) a[i] = tmp[i];
      }
      if (r + step <=n && sum <= t) r += step, step *= 2, should_sort = 1;
      else step /= 2, should_sort = 0;
    }
    cnt ++;
  }
  return cnt;
}

int main() {
  int k;
  cin >> k;

  while (k--) {
    cin >> n >> m >> t;
    for (int i = 0; i < n; i ++) cin >> a[i];
    printf("%d\n", solve());
  }
}

// emm，还是要思考怎么用归并减少复杂度，不然大数据会tle