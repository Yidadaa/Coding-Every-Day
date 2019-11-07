#include <iostream>
#include <algorithm>

using namespace std;

int a[500010];
int tmp[500010];
int sort_tmp[500010];
int n, m;
long long t;

void merge_sort(int l, int m, int r) {
  // 归并排序，从tmp中读数据，写到a中
  sort(a + m, a + r);
  int i = l, j = m;
  for (int k = l; k < r; k ++) {
    if (j >= r || (i < m && a[i] < a[j])) sort_tmp[k] = a[i++];
    else sort_tmp[k] = a[j++];
  }
  for (int k = l; k < r; k ++) a[k] = sort_tmp[k];
}

void print_arr(int* a, int n) {
  for (int i = 0; i < n; i ++) cout << a[i] << ' ';
}

int solve() {
  int cnt = 0;
  for (int l = 0, r = 0; l < n; l = r) {
    int step = 1;
    long long sum = 0;
    while (step > 0) {
      sum = 0;
      if (r + step <= n) {
        for (int i = r; i < r + step; i ++) tmp[i] = a[i];
        merge_sort(l, r, r + step);
        // sort(a + l, a + r + step);

        int i = l, j = r + step - 1;
        for (int t = 0; t < m && i < j; t ++, i ++, j --) {
          sum += (a[i] - a[j]) * (a[i] - a[j]);
        }
        for (int i = r; i < r + step; i ++) a[i] = tmp[i];
        if (sum > t) step /= 2;
        else r += step, step *= 2;
      } else step /= 2;
    }
    printf("%d-%d-%d\n", l, r, sum);
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