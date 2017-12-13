'''
绘制图形
'''
import matplotlib as mpl
import matplotlib.pyplot as plt
import json

mpl.style.use('classic')
# plt.rcParams['font.sans-serif'] = ['思源宋体 CN'] #用来正常显示中文标签
# plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号

fig = plt.figure()

with open('./data/res.json') as f:
    res = json.loads(f.read())
n = 40
x = [x[1] for x in res[0:n]]
# sk_a = [x[2][0] for x in res[0:n]]
# sk_f1 = [x[2][3] for x in res[0:n]]
me_a = [x[3][0] for x in res[0:n]]
me_p = [x[3][1] for x in res[0:n]]
me_r = [x[3][2] for x in res[0:n]]
me_f1 = [x[3][3] for x in res[0:n]]
# me_time = [-x[4] for x in res[0:n]]

# plt.plot(x, sk_f1, label='sk-F1', color='#618D8A')
# plt.plot(x, sk_a, label='sk-accuracy', color='#E46D69')
ax1 = fig.add_subplot(111)
ax1.plot(x, me_f1, label='F1')
ax1.plot(x, me_a, label='accuracy')
ax1.plot(x, me_p, label='precision')
ax1.plot(x, me_r, label='recall')
plt.xlabel('lambda')
plt.ylabel('rate')

# ax2 = fig.add_subplot(212)
# ax2.plot(x, me_time, label='time', color='#618D8A')
# plt.xlabel('rate of feature words')
# plt.ylabel('seconds')

ax1.legend(shadow=True, loc='best')
# ax2.legend(shadow=True, loc='best')
# plt.show()
plt.savefig('./doc/fig_2.jpg')