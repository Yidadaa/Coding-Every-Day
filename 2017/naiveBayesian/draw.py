'''
绘制图形
'''
import matplotlib.pyplot as plt
import json

with open('./data/res.json') as f:
    res = json.loads(f.read())

x = [x[1] for x in res[0:40]]
sk_a = [x[2][0] for x in res[0:40]]
sk_f1 = [x[2][3] for x in res[0:40]]
me_a = [x[3][0] for x in res[0:40]]
me_f1 = [x[3][3] for x in res[0:40]]

plt.plot(x, sk_f1, label='sk-F1', color='#618D8A')
plt.plot(x, sk_a, label='sk-accuracy', color='#E46D69')
plt.plot(x, me_f1, '-.', label='F1', color='#618D8A')
plt.plot(x, me_a, '-.', label='accuracy', color='#E46D69')

leg = plt.legend(shadow=True)
# plt.show()
plt.savefig('./doc/fig_1.jpg')