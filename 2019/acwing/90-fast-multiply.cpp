#include <iostream>

using namespace std;

typedef long long ll;

int main() {
  ll a, b, p = 0;
  cin >> a >> b >> p;
  
  ll res = 0;
  
  for (; b; b >>= 1) {
    if (b & 1) res = (res + a) % p;
    a = a * 2 % p;
  }
  
  cout << res;
}