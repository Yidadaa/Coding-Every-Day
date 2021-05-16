#include <iostream>
#include <unordered_map>
#include <cstring>

using namespace std;

const int MOD = 1000000007;
const int MAXN = 2e5 * 200;
long long dw[MAXN] = { 0 };
int dt[MAXN][26] = { 0 };
int di = 1;

int solve(int node, char s[256], int i, int n) {
  if (i >= n || !dt[node][s[i] - 'a']) return dw[node];
  return (dw[node] + solve(dt[node][s[i] - 'a'], s, i + 1, n));
}

int main() {
  int n;
  cin >> n;

  char s[256];
  int w;
  while (n --) {
    scanf("%s %d", s, &w);
    int n = strlen(s);
    int node = 1;
    for (int i = 0; i < n; i += 1) {
      char c = s[i] - 'a';
      if (!dt[node][c]) {
        dt[node][c] = ++di;
      }
      node = dt[node][c];
      dw[node] = (dw[node] + w) % MOD;
    }
  }

  int m;
  cin >> m;
  while (m --) {
    scanf("%s %d", s, &w);
    long long res = solve(1, s, 0, strlen(s));
    cout << res * w % MOD << endl;
  }
}

struct DTNode
{
  DTNode* children[128] = { NULL };
  long long w = 0;
};

long long solve2(DTNode *dt, char s[256], int i, int n) {
  if (i >= n || dt->children[s[i]] == NULL) {
    return dt->w;
  }
  return (dt->w + solve2(dt->children[s[i]], s, i + 1, n)) % MOD;
}

int main2() {
  int n;
  cin >> n;
  DTNode* dt = new DTNode();
  char s[256];
  int w;
  while (n --) {
    scanf("%s %d", s, &w);
    int n = strlen(s);
    DTNode* node = dt;
    for (int i = 0; i < n; i += 1) {
      char c = s[i];
      if (node->children[c] == NULL) {
        node->children[c] = new DTNode();
      }
      node = node->children[c];
      node->w = (node->w + w) % MOD;
    }
  }

  int m;
  cin >> m;
  while (m --) {
    scanf("%s %d", s, &w);
    long long res = solve2(dt, s, 0, strlen(s));
    cout << res * w % MOD << endl;
  }
}