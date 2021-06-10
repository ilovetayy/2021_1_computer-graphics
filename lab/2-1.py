import numpy as np

res1 = np.array(list(range(2, 27)))
print(str(res1)+"\n")

res2 = np.reshape(res1, (5,5))
print(str(res2)+"\n")

res2[1:-1, 1:-1] = 0
res3 = res2
print(str(res3)+"\n")

res4 = res3 @ res3
print(str(res4)+"\n")

res5 = res4[0][0] * res4[0][0]
for i in range(1, 5):
    res5 += res4[0][i] * res4[0][i]
print(np.sqrt(res5))
