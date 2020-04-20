def read_ints():
    return list(map(int, input().split(' ')))

def solve():
    t = int(input())
    leap_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    norm_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    leap = [0] * sum(leap_days)
    norm = [0] * sum(norm_days)
    for i, days in enumerate([leap_days, norm_days]):
        count = 0
        month, day = 0, 0
        for d in range(sum(days)):
            count += sum(c == '9' for c in '{}{}'.format(month + 1, day + 1))
            [leap, norm][i][d] = count
            day += 1
            if day >= days[month]:
                day = 0
                month += 1

    def is_leap(y):
        return y % 400 == 0 or y % 4 == 0 and y % 100 > 0

    def get_day_index(y, m, d):
        days = [norm_days, leap_days][int(is_leap(y))]
        return sum(days[:m]) + d

    def count_year(y):
        count = 0
        while y:
            count += int(y % 10 == 9)
            y //= 10
        return count

    def count_range(y, sm, sd, em, ed):
        count = [norm, leap][int(is_leap(y))]
        st_day = get_day_index(y, sm, sd)
        ed_day = get_day_index(y, em, ed)
        st_count = 0 if st_day == 0 else count[st_day - 1]
        ed_count = count[ed_day]
        return ed_count - st_count + count_year(y) * (ed_day - st_day + 1)

    for i in range(t):
        sy, sm, sd, ey, em, ed = read_ints()
        sm, sd, em, ed = sm - 1, sd - 1, em - 1, ed - 1
        ret = 0
        for y in range(sy + 1, ey):
            cy = count_year(y)
            if is_leap(y): ret += leap[-1] + cy * 366
            else: ret += norm[-1] + cy * 365
        if sy == ey:
            ret += count_range(sy, sm, sd, em, ed)
        else:
            # 开始年份
            ret += count_range(sy, sm, sd, 11, 30)
            ret += count_range(ey, 0, 0, em, ed)
        print(ret)

solve()

'''
4
2017 04 09 2017 05 09
2100 02 01 2100 03 01
9996 02 01 9996 03 01
2000 01 01 9999 12 31

1
2017 04 09 2017 05 09

1
2010 04 09 2017 05 09

32
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
2000 01 01 9999 12 31
'''