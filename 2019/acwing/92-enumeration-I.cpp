#include <iostream>

using namespace std;

int LOG2[37];

int main() {
  int n = 0;
  cin >> n;
  
  for (int i = 0; i < 15; i++) {
    LOG2[(1 << i) % 37] = i;
  }
  
  for (int i = 0; i < 1 << n; i++) {
    int number = i;
    while (number > 0) {
      int lowBit = number & (-number);
      number -= lowBit;
      cout << LOG2[lowBit % 37] + 1 << ' ';
    }
    cout << endl;
  }
}

// 递归实现的枚举比较简单，这里的代码是使用二进制状态压缩 + lowbit 的版本
// 常数空间复杂度，时间复杂度保持一致