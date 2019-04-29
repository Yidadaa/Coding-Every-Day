class Solution:
    def intToRoman(self, num: int) -> str:
        d = {
            1000: 'M',
            900: 'CM',
            500: 'D',
            400: 'CD',
            100: 'C',
            90: 'XC',
            50: 'L',
            40: 'XL',
            10: 'X',
            9: 'IX',
            5: 'V',
            4: 'IV',
            1: 'I'
        }
        ret = ''
        while num > 0:
            mins = 'I' * (num + 1)
            minn = num + 1
            thex = 1
            for x in d:
                n = num // x
                if n > 0 and n < minn and len(d[x]) < len(mins):
                    minn = n
                    mins = d[x]
                    thex = x
            ret += mins * minn
            num -= thex * minn
        return ret
