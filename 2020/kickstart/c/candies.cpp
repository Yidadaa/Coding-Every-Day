#include <iostream>
#include <cstring>

using namespace std;

const int MAXN = 2 * 1e5 + 10;
typedef long long ll;

class Tree
{
public:
    int nums[MAXN];
    ll aarr[MAXN + 1];
    ll sarr[MAXN + 1];
    int n;
    ll val_sum = 0;
    ll sweet_sum = 0;

    Tree() {}

    void reset(int nums[], int n)
    {
        memset(aarr, 0, sizeof(ll) * (MAXN + 1));
        memset(sarr, 0, sizeof(ll) * (MAXN + 1));
        this->n = n;
        for (int i = 0; i < n; i += 1)
        {
            add(i + 1, nums[i]);
            this->nums[i] = nums[i];
            // cout << aarr[i + 1] << ' ' << sarr[i + 1] << ' ' << nums[i] << endl;
        }
    }

    void add(int i, int val)
    {
        int neg = i % 2 ? 1 : -1;
        ll aval = val * neg;
        ll sval = val * neg * i;
        while (i <= n)
        {
            aarr[i] += aval;
            sarr[i] += sval;
            i += (i & -i);
        }
    }

    void update(int i, int val)
    {
        add(i, val - nums[i - 1]);
        nums[i - 1] = val;
    }

    void get(int i)
    {
        val_sum = 0, sweet_sum = 0;
        while (i > 0)
        {
            val_sum += aarr[i];
            sweet_sum += sarr[i];
            i -= (i & -i);
        }
    }

    ll sum(int i, int j)
    {
        get(j);
        ll vsum = val_sum, ssum = sweet_sum;
        // cout << ssum << " " <<  vsum << endl;
        get(i - 1);
        vsum -= val_sum;
        ssum -= sweet_sum;
        // cout << sweet_sum << " " <<  val_sum << endl;
        return (ssum - (i - 1) * vsum) * (i % 2 ? 1 : -1);
    }
};

int nums[MAXN];

int main()
{
    int T;
    cin >> T;

    Tree tree;

    for (int t = 1; t <= T; t += 1)
    {
        int n, q;
        cin >> n >> q;
        for (int i = 0; i < n; i += 1) cin >> nums[i];

        tree.reset(nums, n);
        ll ret = 0;
        for (int i = 0; i < q; i += 1)
        {
            char action;
            int a, b;
            cin >> action >> a >> b;
            if (action == 'Q') ret += tree.sum(a, b);
            else if (action == 'U') tree.update(a, b);
            // cout << action << endl;
        }
        cout << "Case #" << t << ": " << ret << endl;
    }
}

/*
2
5 4
1 3 9 8 2
Q 2 4
Q 5 5
U 2 10
Q 1 2
3 3
4 5 5
U 1 2
U 1 7
Q 1 2

1
5 4
1 3 9 8 21 3 9 8 21 3 9 8 21 3 9 8 2
Q 2 4
Q 5 5
U 2 10
Q 1 2
Q 10 25
U 12 13
*/