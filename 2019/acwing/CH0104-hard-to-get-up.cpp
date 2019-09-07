#include <iostream>
#include <string>

using namespace std;

pair<string, int> op_t[100001];
int n = 0, m = 0;


int do_op(int bit, int num) {
  for (int i = 0; i < n; i++) {
    int t_i_bit = op_t[i].second >> bit & 1;
    if (op_t[i].first == "AND") num &= t_i_bit;
    else if (op_t[i].first == "OR") num |= t_i_bit;
    else num ^= t_i_bit;
  }
  return num;
}

int main() {  
  cin >> n >> m;

  for (int i = 0; i < n; i++) {
    string op; int t;
    cin >> op >> t;
    op_t[i] = make_pair(op, t);
  }

  int _m = 0, ans = 0;
  for (int bit = 29; bit >= 0; bit--) {
    int set_zero = do_op(bit, 0);
    int set_one = do_op(bit, 1);
    if (_m + (1 << bit) <= m && set_zero < set_one) {
      _m += 1 << bit;
      ans += set_one << bit;
    } else {
      ans += set_zero << bit;
    }
  }

  cout << ans << endl;}