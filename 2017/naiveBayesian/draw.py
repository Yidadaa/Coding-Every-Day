'''
绘制图形
'''
import matplotlib.pyplot as plt
import json

with open('./data/res.json') as f:
    res = json.loads(f.read())

x = [x[1] for x in res[0:40]]
me_a = [x[3][0] for x in res[0:40]]
me_f1 = [x[3][3] for x in res[0:40]]
me_p = [x[3][2] for x in res[0:40]]
me_r = [x[3][1] for x in res[0:40]]
plt.plot(x, me_f1, label='F1')
plt.plot(x, me_a, label='accuracy')
plt.plot(x, me_p, label='precision')
plt.plot(x, me_r, label='recall')
plt.legend(loc='upper right')
plt.show()
