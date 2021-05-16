#include <iostream>
#include <map>

using namespace std;

int get(map<int, int> &m, int x) {
  return m.count(x) ? m[x] : 0;
}

int main() {
  int n;
  cin >> n;

  map<int, int> m;
  for (int i = 0, s = 0, t = 0; i < n; i += 1) {
    cin >> s >> t;
    m[s] = get(m, s) + 1;
    m[t] = get(m, t) - 1;
  }

  int res = 0, count = 0, last = 0;
  for (auto it : m) {
    cout << it.first << ' ' << it.second << endl;
    count += it.second;
    if (count > 0) {
      res += it.first - last;
    }
    last = it.first;
  }

  cout << res << endl;
}