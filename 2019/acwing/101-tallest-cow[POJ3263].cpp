#include <iostream>
#include <map>
#include <cstring>

using namespace std;

const int N = 10010;
int cows[N];
map<int, int> exist;

int main() {
  int n, p, h, m;

  cin >> n >> p >> h >> m;

  memset(cows, 0, sizeof(cows));
  
  cows[1] = h;

  int a, b;
  while (m--) {
    cin >> a >> b;
    if (a > b) swap(a, b);
    if (exist[a] != b) {
      cows[a + 1] -= 1;
      cows[b] += 1;
      exist[a] = b;
    }
  }

  for (int i = 1; i <=n; i++) {
    cows[i] += cows[i - 1];
    cout << cows[i] << endl;
  }
}

// 差分序列来描述区间操作