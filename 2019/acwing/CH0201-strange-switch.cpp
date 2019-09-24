#include <iostream>
#include <cstring>

using namespace std;

char s[10][10];
char s_[10][10];

int d[5][2] = {
  {0, 0}, {-1, 0}, {1, 0},
  {0, -1}, {0, 1}
};

void kick(int x, int y) {
  // kick button
  for (int i = 0; i < 5; i++) {
    int x_ = x + d[i][0];
    int y_ = y + d[i][1];
    if (x_ > -1 && x < 5 && y_ > -1 && y_ < 5) {
      s_[x_][y_] ^= 1; // 直接异或就可以完成状态切换
    }
  }
}

int solve() {
  int ret = 100000; // 最小切换次数

  for (int i = 0; i < 1 << 5; i++) {
    int count = 0; // 当前切灯数
    memcpy(s_, s, sizeof(s));

    for (int j = 0; j < 5; j++) {
      if (i >> j & 1) {
        count++;
        kick(0, j);
      }
    }

    // 根据第一行状态往后递推
    for (int j = 0; j < 4; j++) {
      for (int k = 0; k < 5; k++) {
        if (s_[j][k] == '0') {
          count++;
          kick(j + 1, k);
        }
      }
    }

    // 判断最后一行是否满足条件
    int count_one = 0;
    for (int j = 0; j < 5; j++) {
      count_one += s_[4][j] - '0';
    }

    // 如果全为1，则保存最小遍历次数
    if (count_one == 5) {
      ret = min(ret, count);
    }
  }

  return ret > 6 ? -1 : ret;
}

int main() {
  int n;
  cin >> n;
  while (n--) {
    for (int i = 0; i < 5; i++) {
      cin >> s[i];
    }

    cout << solve() << endl;
  }

  return 0;
}