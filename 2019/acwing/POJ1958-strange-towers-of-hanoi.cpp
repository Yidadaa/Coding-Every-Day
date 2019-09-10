#include <iostream>
#include <cstring>

using namespace std;

int d[13]; // pre-calculate for three towers
int f[13];
int MAX_INT = 1 << 30;

void solve(int n) {
  for (int i = 2; i < n; i++) {
    for (int j = 1; j < i; j++) {
      f[i] = min(f[i], 2 * f[j] + d[i - j]);
    }
  }
}

int main() {
  memset(f, 0x3f, sizeof(f));

  d[0] = 0;
  f[0] = 0;
  f[1] = 1;

  for (int i = 1; i < 13; i++) {
    d[i] = 2 * d[i - 1] + 1;
  }

  solve(13);

  for (int i = 1; i < 13; i++) {
    cout << f[i] << endl;
  }
}