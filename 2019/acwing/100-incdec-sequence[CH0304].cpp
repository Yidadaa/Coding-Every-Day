#include <iostream>
#include <algorithm>

using namespace std;

typedef long long ll;

const int N = 100010;

int a[N];

int main() {
  int n;
  
  cin >> n;
  
  for (int i = 1; i <= n; i++) cin >> a[i];
  for (int i = n; i > 1; i--) a[i] -= a[i - 1];
  
  ll p = 0, q = 0;
  for (int i = 2; i <= n; i++) {
    if (a[i] > 0) p += a[i];
    else q -= a[i];
  }
  
  cout << max(p, q) << endl << abs(p - q) + 1;
}
