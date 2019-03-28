import random
from math import sqrt

m = 0
s = 0
v = []
l = 0
p = 0

for _ in range(200):
    v.append(random.expovariate(0.003)/2)
    m += v[-1]/200
    if v[-1]<30:
        l+=1
    if v[-1]>250:
        p+=1

for i in range(200):
    s += ((v[i]-m)**2)/200

s = sqrt(s)

print(m)
print(s)
print(max(v))
print(min(v))
print(l)
print(p)

