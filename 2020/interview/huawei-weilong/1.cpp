#include <iostream>
#include <string>
#include <cstring>

using namespace std;

int main() {
  int n, m, t, p;
  string seq;

  cin >> n >> m >> t >> p;
  cin >> seq;

  int last_warning_time = -1;
  int count[2] = { 0, 0 };
  int periods[2] = { n, m };
  int condition[2] = { n, t };
  int *state = new int[seq.size()];
  memset(state, 0, sizeof(state));

  for (int si = 0; si <= seq.size(); si += 1) {
    char c = seq[si];
    if (c == 'f') {
      for (int i = 0; i < 2; i ++) count[i] += 1;
    }
    for (int i = 0; i < 2; i ++) {
      if (periods[i] < si) continue;
      count[i] -= int(seq[si - periods[i]] == 'f');
    }

    for (int i = 0; i < 2; i += 1) {
      if (count[i] >= condition[i]) {
        // check warning gap
        state[si] = 1;
        last_warning_time = si;
      }
    }

    if (si - last_warning_time + 1 >= p) break;
  }

  int ret = 0, si = 0;
  while (si < seq.size()) {
    int count = 0;
    while (si + count < seq.size() && state[si + count]) {
      count += 1;
    }
    ret = max(ret, count);
    si += count + 1;
  }

  cout << si << endl;
}

/**
3 10 6 3
nffnffffffnnnnn
**/