
def count(s):
    ret = {}
    for c in s:
        if c not in ret:
            ret[c] = 0
        ret[c] += 1
    return ret

def solution(s):
    cts = count(s)
    n = len(s)
    max_part = min(cts.values())
    
    for part in range(max_part, 1, -1):
        if n % part != 0:
            continue
        
        # check first part
        part_len = n // part
        head_part = s[:part_len]
        checked = True
        
        for i in range(0, n, part_len):
            checked = checked and s[i:i + part_len] == head_part
        
        if checked:
            return print(part)
    print(1)

for case in ['abcabcabcabc', 'abccbaabccba']:
    print(case)
    solution(case)