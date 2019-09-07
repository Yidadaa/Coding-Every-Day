#include <iostream>

using namespace std;

int n;
int order[10], chosen[10];

void do_perm(int index) {
  if (index == n) {
    for (int i = 0; i < n; i++) {
      cout << order[i] + 1 << ' ';
    }
    cout << endl;
    return;
  }
  
  for (int i = 0; i < n; i++) {
    if (chosen[i]) continue;
    
    order[index] = i;
    chosen[i] = 1;
    
    do_perm(index + 1);
    
    chosen[i] = 0;
  }
}

int main() {
  cin >> n;
  do_perm(0);
}

// 全排列递归，跟以前用过的不一样……使用了 order 数组来标记输出顺序