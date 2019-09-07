#include <iostream>

using namespace std;

typedef long long ll;

int main() {
  ll a, b, p = 0;
  cin >> a >> b >> p;
  
  ll res = 1 % p;
  
  for (; b; b >>= 1) {
    if (b & 1) res = (ll) res * a % p;
    a = (ll) a * a % p;
  }
  
  cout << res;
}