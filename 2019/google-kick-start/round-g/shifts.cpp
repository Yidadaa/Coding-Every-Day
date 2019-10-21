#include <iostream>

using namespace std;

typedef long long ll;

int a[30], b[30];

ll pow(int x, int y) {
  ll ret = 1;
  while (y--) ret *= x;
  return ret;
}

bool check(int n, int h, int a[], int b[], int k) {
  ll c_a = 0, c_b = 0;
  for (int i = n - 1; i >= 0; i--) {
    int state = (k % 3) + 1;
    int has_a = state & 1;
    int has_b = (state >> 1) & 1;
    if (has_a + has_b < 1) break;
    k /= 3;
    c_a += has_a * a[i];
    c_b += has_b * b[i];
    if (c_a >= h && c_b >= h) break;
  }
  return c_a >= h && c_b >= h;
}

int main() {
  int t;
  cin >> t;

  for (int c = 1; c <= t; c++) {
    int n, h;
    cin >> n >> h;

    int s_a = 0, s_b = 0;

    for (int i = 0; i < n; i++) cin >> a[i], s_a += a[i];
    for (int i = 0; i < n; i++) cin >> b[i], s_b += b[i];

    ll ret = 0;

    if (s_a >= h && s_b >= h) {
      ll max_n = pow(3, n);
      for (int i = 1; i <= max_n; i++) {
        if (check(n, h, a, b, i)) ret += 1;
      }
    }

    printf("Case #%d: %lld\n", c, ret);
  }
}