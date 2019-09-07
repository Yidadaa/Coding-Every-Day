#include <iostream>
#include <cstring>

using namespace std;

const int N = 20, M = 1 << 20;

int state[M][N];
int weight[N][N];

int main() {
  memset(state, 0x3f, sizeof(state));
  
  int n = 0;
  cin >> n;
  
  for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++)
      cin >> weight[i][j];
      
  state[1][0] = 0;
  
  for (int i = 0; i < M; i++)
    for (int j = 0; j < n; j++) if (i >> j & 1)
      for (int k = 0; k < n; k++) if ((i ^ 1 << j) >> k & 1)
        state[i][j] = min(state[i][j], state[i ^ 1 << j][k] + weight[k][j]);
        
  cout << state[(1 << n) - 1][n - 1];
}

/*
 * 主要用到状态压缩，每个节点只有走过和没有走过两个状态，总共有 n 个节点
 * 那么总状态数就是 2^n 个，然后当前所处的节点共有 n 个取值，所以状态矩阵就是 2^n * n 个
 * 只需要遍历所有状态，然后选取最小的状态值更新状态表即可。
 */