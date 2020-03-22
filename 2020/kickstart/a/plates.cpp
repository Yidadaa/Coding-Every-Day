#include <iostream>
#include <cstring>

using namespace std;

const int N = 51, P = 1501, K = 31;
int dp[N][P][K];

// 还是 cpp 好
int main()
{
  int t = 0;
  cin >> t;
  for (int c = 1; c <= t; c += 1)
  {
    memset(dp, 0, sizeof(int) * N * P * K);
    int n, k, p;
    cin >> n >> k >> p;
    for (int i = 0; i < n; i += 1)
    {
      int s = 0;
      for (int j = 0; j < k + 1; j += 1)
      {
        if (j > 0)
        {
          int x = 0;
          cin >> x;
          s += x;
        }
        if (i == 0)
        {
          if (j < p + 1) dp[i][j][j] = s;
          continue;
        }
        for (int tp = j; tp < p + 1; tp += 1)
        {
          int m = 0;
          for (int ki = 0; ki < k + 1; ki += 1) m = max(m, dp[i - 1][tp - j][ki]);
          dp[i][tp][j] = m + s;
        }
      }
    }
    int ret = 0;
    for (int ki = 0; ki < k + 1; ki += 1) ret = max(ret, dp[n - 1][p][ki]);
    cout << "Case #" << c << ": " << ret << endl;
  }
}