#include <iostream>

using namespace std;

int a[505][505];
int b[505][505];
int t[500 * 500 + 5];
int main() {
  long long n, m;
  cin >> n >> m;

  for (int i = 1; i <= n; i += 1)
    for (int j = 1; j <= n; j += 1)
      cin >> a[i][j], b[i][j] = 0;

  t[1] = 1, t[2] = 2;
  int step = 3;
  while (b[t[step - 1]][t[step - 2]] == 0) {
    int i = step - 1, j = step - 2;
    t[step ++] = a[t[i]][t[j]];
    b[t[i]][t[j]] = step - 1;
    a[t[i - 1]][t[j - 1]] = -1;
  }
  int head = b[t[step - 1]][t[step - 2]];
  if (m <= head) {
    cout << t[m] << endl;
  } else {
    int rec_step = step - head;
    cout << t[(m - head) % rec_step + head] << endl;
  }
}