#include <iostream>
#include <cstring>
#include <cmath>

using namespace std;

typedef long long LL;
typedef pair<LL, LL> PLL;

PLL solve(LL N, LL X) {
  if (N == 0) return {0, 0};
  LL length = 1ll << N - 1; // 城市的边长
  LL size = 1ll << 2 * N - 2; // N - 1 级城市的规模
  auto p = solve(N - 1, X % size);
  // 得到 N - 1 级坐标后，将其变换到 N 级城市坐标
  LL x = p.first, y = p.second;
  LL index = X / size; // 计算在 N 级城市中的索引，范围是[0, 3]
  if (index == 0) {
    // 说明在左上角，第 N - 1 级变换到第 N 级 时，第 0 块城市会沿着 y = x 这条直线翻转
    return {y, x};
  } else if (index == 1) {
    // N 级右上角只需要经过简单平移
    return {x, y + length};
  } else if (index == 2) {
    // 在右上角基础上向下平移
    return {x + length, y + length};
  } else if (index == 3) {
    // 在右下角基础上逆时针旋转 90 度
    return {length - y - 1 + length, length - x - 1};
  }
}

int main() {
  int n;
  cin >> n;

  while (n--) {
    LL N, A, B;
    cin >> N >> A >> B;
    auto pa = solve(N, A - 1);
    auto pb = solve(N, B - 1);
    double dx = pa.first - pb.first;
    double dy = pa.second - pb.second;
    printf("%.0lf\n", sqrt(dx * dx + dy * dy) * 10);
  }
  return 0;
}