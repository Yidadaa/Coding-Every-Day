#include <iostream>

using namespace std;

int a[250000];
int tmp[250000];

long long count_reverse(int n) {
  long long ret = 0;
  for (int step = 1; step < n; step <<= 1) {
    for (int l = 0; l < n; l += step * 2) {
      int m = min(l + step, n);
      int r = min(m + step, n);
      int li = l, ri = m;
      for (int i = l; i < r; i += 1) {
        bool cond = (li >= m) || (ri < r && a[li] > a[ri]);
        tmp[i] = cond ? a[ri++] : a[li++];
        if (cond) ret += m - li;
      }
      for (int i = l; i < r; i += 1) a[i] = tmp[i];
    }
  }
  return ret;
}

int main() {
  int n;
  while (cin >> n) {
    n *= n;
    
    int count = 0;
    for (int i = 0; i < 2; i += 1) {
      for (int j = 0, offset = 0; j < n; j += 1) {
        scanf("%d", &a[j - offset]);
        if (a[j] == 0) offset = 1;
      }
      count += count_reverse(n) & 1;
    }

    printf("%s\n", count & 1 ? "NIE" : "TAK");
  }
  
  return 0;
}