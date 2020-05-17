import random

def sovle():
    n = 100000
    data = [random.randint(1, 100) for i in range(n)]
    nq = n
    content = []
    ns, qs = 0, 0
    for i in range(nq):
        action = 'Q' if random.random() > 0.5 else 'U'
        if action == 'Q':
            qs += 1
            a = random.randint(1, n)
            b = random.randint(a, n)
        else:
            ns += 1
            a = random.randint(1, n)
            b = random.randint(1, 100)
        content.append('{} {} {}'.format(action, a, b))
    with open('data.txt', 'w') as f:
        f.write('1\n')
        f.write('{} {}\n'.format(n, ns + qs))
        f.write(' '.join([str(x) for x in data]) + '\n')
        f.write('\n'.join(content))

sovle()