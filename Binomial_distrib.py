import random
import numpy as np
import matplotlib.pyplot as plt
import scipy.special as sp

random.seed()

# j = random.choices([True, False], [95, 5], k=10)
#
# print(j)
# print()
#
k = random.choices([True, False], [95, 5], k=50)

print(k)
print()
#
# l = random.choices([True, False], [95, 5], k=1000)
#
# print(l)

x_values = [x/50 for x in range(1, 51)]


def binomial_proba(T, F, proba):
    binomial = sp.comb(T+F, F)
    prob = binomial * proba**T * (1-proba)**F
    return prob


# JT = j.count(True)
# JF = j.count(False)
#
KT = k.count(True)
KF = k.count(False)

# print(sp.comb(50, 48)*0.95**48*(1-0.95)**2)
# print(binomial_proba(48, 2, 0.95))
y_values = [binomial_proba(KT, KF, x) for x in x_values]

x_positions = [x for x, _ in enumerate(x_values)]

print(x_values)
print(y_values)

print(binomial_proba(KT, KF, 0.5))

plt.bar(x_positions, y_values)

plt.show()