#include <iostream>
#include <unordered_map>
#include <algorithm>
#include <cmath>
#include <cstring>

using namespace std;

const int MAXN = 100005;
const int MAXT = 100 * MAXN;
int nums[MAXN];
int table[2 * MAXT];

int main()
{
    int T;
    scanf("%d", &T);

    for (int t = 1; t <= T; t += 1)
    {
        int n;
        scanf("%d", &n);

        int s = 0, mi = 0, ma = 0;

        for (int i = 0; i < n; i += 1)
        {
            scanf("%d", nums + i);
            if (nums[i] >= 0) ma += nums[i];
            else mi -= nums[i];
        }

        int R = (int)sqrt(mi + ma);
        int* ks = new int[R + 1];
        for (int i = 0; i <= R; i += 1)
        {
            ks[i] = i * i;
        }

        memset(table, 0, 2 * MAXT * sizeof(int));

        table[MAXT] = 1;
        s = 0;
        long long count = 0;
        for (int i = 0; i < n; i += 1)
        {
            s += nums[i];
            for (int j = 0; j <= R; j += 1)
            {
                count += table[s - ks[j] + MAXT];
            }
            table[s + MAXT] += 1;
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