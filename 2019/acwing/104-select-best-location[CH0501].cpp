#include <iostream>
#include <algorithm>

using namespace std;

int a[100005];

int main() {
  int n;
  cin >> n;

  for (int i = 0; i < n; i++) cin >> a[i];

  sort(a, a + n);

  int l, r;
  if (n & 1) {
    l = r = n >> 1;
  } else {
    r = n >> 1;
    l = r - 1;
  }

  int mid = (a[l] + a[r]) / 2;

  long long ret;

  for (int i = 0; i < n; i++) ret += abs(a[i] - mid);

  cout << ret;
}