#include <iostream>
#include <cstring>

using namespace std;

int s[5001][5001];

int main() {
  int n, r;
  cin >> n >> r;

  memset(s, 0, sizeof(s));

  // 读入数据
  int x, y, w;
  int max_x = 0, max_y = 0;
  while (n--) {
    cin >> x >> y >> w;
    s[x][y] += w;
    max_x = max(max_x, x);
    max_y = max(max_y, y);
  }

  // 计算二维前缀和
  int d[3][3] = {
    {-1, 0, 1},
    {0, -1, 1},
    {-1, -1, -1}
  };

  for (int i = 0; i <= max_x; i++) {
    for (int j = 0; j <= max_y; j++) {
      for (int k = 0; k < 3; k++) {
        int dx = i + d[k][0];
        int dy = j + d[k][1];
        if (dx >= 0 && dx <= 5000 && dy >= 0 && dy <= 5000) {
          s[i][j] += d[k][2] * s[dx][dy];
        }
      }
    }
  }

  // 计算炸弹覆盖范围最大值
  int sd[4][3] = {
    {0, 0, 1},
    {-r, 0, -1},
    {0, -r, -1},
    {-r, -r, 1}
  };
  
  int min_x = min(max_x, r - 1);
  int min_y = min(max_y, r - 1);

  int ret = 0;
  for (int i = min_x; i <= max_x; i++) {
    for (int j = min_y; j <= max_y; j++) {
      int sum = 0;
      for (int k = 0; k < 4; k++) {
        int dx = i + sd[k][0];
        int dy = j + sd[k][1];
        if (dx >= 0 && dx <= 5000 && dy >=0 && dy <= 5000) {
          sum += sd[k][2] * s[dx][dy];
        }
      }
      ret = max(ret, sum);
    }
  }

  cout << ret << endl;
}