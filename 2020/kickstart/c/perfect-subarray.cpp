#include <iostream>
#include <unordered_map>
#include <algorithm>
#include <cmath>

using namespace std;

int nums[100005];

int main()
{
    int T;
    scanf("%d", &T);

    for (int t = 1; t <= T; t += 1)
    {
        int n;
        scanf("%d", &n);

        unordered_map<int, int> table;

        int s = 0, mi = 0, ma = 0;
        int R = 0;

        for (int i = 0; i < n; i += 1)
        {
            scanf("%d", nums + i);
            s += nums[i];
            ma = max(nums[i], max(s, ma));
            mi = min(nums[i], min(s, mi));
            R = max(R, ma - mi);
        }

        R = (int)sqrt(R);
        int* ks = new int[R + 1];
        for (int i = 0; i <= R; i += 1)
        {
            ks[i] = i * i;
        }

        table[0] = 1;
        s = 0;
        int count = 0;
        for (int i = 0; i < n; i += 1)
        {
            s += nums[i];
            for (int j = 0; j <= R; j += 1)
            {
                if (table.count(s - ks[j]) == 1) count += table[s - ks[j]];
                if (table.count(s) == 0) table[s] = 0;
            }
            table[s] += 1;
        }

        cout << "Case #" << t << ": " << count << endl;

        delete ks;
    }
}

/*
3
3
2 2 6
5
30 30 9 1 30
4
4 0 0 16

1
3 
2 2 6
*/