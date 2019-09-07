#include <iostream>

using namespace std;

int n, m;

void do_perm(int count, int cur, int state) {
  if (count == 0) {
    for (int i = 0; state > 0; state >>= 1, i++)
      if (state & 1) cout << i + 1 << ' ';
    cout << endl;
    return;
  }
  
  if (n - cur < count) return;
  
  do_perm(count - 1, cur + 1, state + (1 << cur));
  do_perm(count, cur + 1, state);
}

int main() {
  cin >> n >> m;
  do_perm(m, 0, 0);
}

// 使用二进制状态压缩，优化内存占用