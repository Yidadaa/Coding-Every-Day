#include <iostream>
#include <queue>

using namespace std;

int meds[10000];

int main() {
  int n;
  cin >> n;

  while (n--) {
    int index, num;
    cin >> index >> num;

    priority_queue<int, vector<int>, less<int>> lq;
    priority_queue<int, vector<int>, greater<int>> gq;
    int med = -10000000, in;
    for (int i = 1; i <= num; i++) {
      cin >> in;

      if (in > med) gq.push(in);
      else lq.push(in);

      // 调整数值
      while (abs(int(lq.size()) - int(gq.size())) > (i & 1)) {
        if (lq.size() > gq.size()) {
          gq.push(lq.top());
          lq.pop();
        } else {
          lq.push(gq.top());
          gq.pop();
        }
      }
      med = lq.size() < gq.size() ? gq.top() : lq.top();
      if (i & 1) meds[i >> 1] = med;
    }
    
    printf("%d %d\n", index, (num + 1) >> 1);

    for (int i = 0; i < ((num + 1) >> 1); i++) {
      printf("%d", meds[i]);
      printf((i + 1) % 10 ? " " : "\n");
    }

    if ((num + 1) >> 1 % 10) printf("\n");
  }
}