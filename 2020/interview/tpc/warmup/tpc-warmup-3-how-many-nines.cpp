#include <iostream>
#include <string>
#include <cstring>

using namespace std;

const int MONTHS = 12;
const int DAYS = 31;
int leap_days[MONTHS] = {31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
int norm_days[MONTHS] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
int count_md[MONTHS][DAYS];
long int pre_sum[10000][MONTHS][DAYS];

int count_int(int n)
{
    int ret = 0;
    while (n > 0) ret += (int)(n % 10 == 9), n /= 10;
    return ret;
}

int is_leap(int y) {
    return y % 400 == 0 || y % 4 == 0 && y % 100 > 0;
}

void compute(int days[MONTHS], int day_sum[][DAYS], int day_count)
{
    int month = 0, day = 0, count = 0;
    while (month < MONTHS)
    {
        count_md[month][day] = count_int(month + 1) + count_int(day + 1);
        day += 1;
        if (day >= days[month]) day = 0, month += 1;
    }
}

void pre_compute()
{
    compute(leap_days, count_md, 366);
    int y = 2000, m = 0, d = 0;
    int count_year = 0;
    long int count = 0;
    int* days = leap_days;
    while (y < 10000)
    {
        count += count_year + count_md[m][d];
        pre_sum[y][m][d] = count;
        if (++d >= days[m]) d = 0, m += 1;
        if (m >= 12)
        {
            m = 0, y += 1;
            days = is_leap(y) ? leap_days : norm_days;
            count_year = count_int(y);
        }
    }
}

int main()
{
    int t;
    cin >> t;
    pre_compute();
    for (int i = 0; i < t; i += 1)
    {
        int sy, sm, sd, ey, em, ed;
        cin >> sy >> sm >> sd >> ey >> em >> ed;
        long int ret = pre_sum[ey][em - 1][ed - 1] - pre_sum[sy][sm - 1][sd - 1];
        ret += count_int(sy) + count_int(sm) + count_int(sd);
        printf("%ld\n", ret);
    }
}