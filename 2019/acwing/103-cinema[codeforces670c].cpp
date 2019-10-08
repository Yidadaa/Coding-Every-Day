#include <iostream>
#include <unordered_map>

using namespace std;

int movie[200010], text[200010];

int main() {
  unordered_map<int, int> count;

  int n;
  cin >> n;

  int tmp;
  while (n--) {
    cin >> tmp;
    if (count.count(tmp) == 0) count[tmp] = 1;
    else count[tmp] += 1;
  }

  cin >> n;

  for (int i = 0; i < n; i++) cin >> movie[i];
  for (int i = 0; i < n; i++) cin >> text[i];

  int ml, tl;
  int mc = 0, tc = 0, index = -1;
  for (int i = 1; i <= n; i++) {
    ml = movie[i - 1];
    tl = text[i - 1];

    if (count[ml] > mc || (count[ml] == mc && count[tl] >= tc)) {
      mc = count[ml];
      tc = count[tl];
      index = i;
    }
  }

  cout << index;
}