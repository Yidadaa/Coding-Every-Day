#include <iostream>
#include <algorithm>
#include <string>

using namespace std;

const int N = 100000;
int row[N], column[N];

long long solve(int arr[], int n, int t) {
  int avg = t / n; // 求解均值
  for (int i = 0; i < n; i++) arr[i] -= avg; // 减去均值
  for (int i = 1; i < n; i++) arr[i] += arr[i - 1]; // 求前缀和

  sort(arr, arr + n); // 排序

  int median = arr[n >> 1], ret = 0; // 求中值
  for (int i = 0; i < n; i++) ret += abs(arr[i] - median); // 求解

  return ret;  
}

int main () {
  int n, m, t;
  cin >> n >> m >> t;

  for (int i = 0, r, c; i < t; i++) {
    cin >> r >> c;
    row[r] ++;
    column[c] ++;
  }

  int flag = 0;
  long long count = 0;

  // 一个trick，减少代码量，但是会降低可读性
  int* args[2][2] = {
    {row, &n}, {column, &m}
  };

  // 使用2位二进制表示flag
  for (int i = 0; i < 2; i++) {
    flag <<= i;
    if (t % *args[i][1] == 0) {
      flag += 1;
      count += solve(args[i][0], *args[i][1], t);
    }
  }

  // 跟flag配套使用
  char* text[] = {
    "impossible", "column", "row", "both"
  };

  printf("%s", text[flag]);
  if (flag > 0) printf(" %lld", count);
}