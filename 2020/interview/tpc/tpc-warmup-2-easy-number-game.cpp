#include <iostream>
#include <algorithm>

using namespace std;

int main()
{
    int t;
    scanf("%d", &t);
    for (int i = 0; i < t; i += 1)
    {
        int n, m;
        scanf("%d %d", &n, &m);
        int* nums = new int[n];
        for (int j = 0; j < n; j += 1)
            scanf("%d", nums + j);
        sort(nums, nums + n);
        int l = 0, r = 2 * m - 1;
        long long int ret = 0;
        while (l < r)
        {
            ret += nums[l] * nums[r];
            l += 1, r -= 1;
        }
        printf("%lld\n", ret);
    }
}